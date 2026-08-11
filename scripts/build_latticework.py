#!/usr/bin/env python3
"""Build a latticework graph of mental models from shared keywords.

Reads the markdown corpus through ``mental_models_kit.corpus`` (there is no
JSON index any more), computes edges between models that share keyword stems
(threshold auto-tuned to land in a reasonable edge-count range), and writes
three artifacts under docs/:

  - latticework.json       full graph (nodes + edges) for a future web viewer
  - latticework.mmd        full Mermaid rendering
  - latticework_core.mmd   curated subgraph of the 15 highest-degree hubs

Deterministic output (sorted everywhere) so CI can drift-check with git diff.
docs/latticework.svg is rendered separately and is not touched here.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from mental_models_kit.corpus import load_models  # noqa: E402

DOCS = REPO / "docs"

# 8 distinct, print-safe colors keyed by category. Unknown categories fall back
# to the last entry. Keys are matched by substring.
CATEGORY_COLORS = [
    ("General Thinking", "#60a5fa"),   # blue
    ("Physics",          "#34d399"),   # green
    ("Systems",          "#f472b6"),   # pink
    ("Mathematics",      "#a78bfa"),   # purple
    ("Economics",        "#fbbf24"),   # amber
    ("Art",              "#fb923c"),   # orange
    ("Warfare",          "#f87171"),   # red
    ("Human",            "#22d3ee"),   # cyan
]
FALLBACK_COLOR = "#9ca3af"


def color_for(category: str) -> str:
    for key, color in CATEGORY_COLORS:
        if key.lower() in category.lower():
            return color
    return FALLBACK_COLOR


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "in", "on", "for", "to", "with",
    "by", "at", "from", "as", "is", "it", "be", "that", "this", "into",
    "how", "why", "what", "its", "their", "our", "your", "any", "all",
}


def norm_keyword(k: str) -> set[str]:
    """Tokenize a keyword phrase into a set of normalized word-stems.

    We treat each keyword as a bag of words so overlapping concepts such as
    "public speaking" and "speaking" still produce a shared token. This is
    what gives the latticework enough edges to be interesting without
    hand-annotating every model.
    """
    k = k.lower()
    k = re.sub(r"[^\w\s-]", " ", k)
    tokens = set()
    for w in k.split():
        w = w.strip("-_")
        if len(w) < 4 or w in STOPWORDS:
            continue
        # crude stem: drop common suffixes
        for suf in ("ing", "ies", "ied", "ness", "ment", "tion", "sion", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 4:
                w = w[: -len(suf)]
                break
        tokens.add(w)
    return tokens


def load_nodes() -> list[dict]:
    """Corpus models reduced to (id, slug, name, category, keyword stems)."""
    nodes = []
    for m in load_models():
        kws: set[str] = set()
        for k in m.keywords:
            kws |= norm_keyword(k)
        kws.discard("")
        nodes.append({
            "id": m.id,
            "slug": m.slug,
            "name": m.name,
            "category": m.category,
            "keywords": kws,
        })
    nodes.sort(key=lambda x: x["id"])
    return nodes


def compute_edges(models: list[dict], threshold: int) -> list[tuple[str, str, int]]:
    # invert: keyword -> [model ids]
    kw_to_models: dict[str, list[str]] = defaultdict(list)
    for m in models:
        for k in m["keywords"]:
            kw_to_models[k].append(m["id"])

    pair_counts: dict[tuple[str, str], int] = defaultdict(int)
    for kw, ids in kw_to_models.items():
        ids = sorted(set(ids))
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pair_counts[(ids[i], ids[j])] += 1

    edges = [(a, b, w) for (a, b), w in pair_counts.items() if w >= threshold]
    edges.sort(key=lambda e: (-e[2], e[0], e[1]))
    return edges


def auto_tune(models: list[dict]) -> tuple[int, list[tuple[str, str, int]]]:
    """Pick lowest threshold >= 2 that yields 150..400 edges; else best-effort."""
    for thr in (2, 3, 4, 5):
        edges = compute_edges(models, thr)
        if 150 <= len(edges) <= 400:
            return thr, edges
    # fallback: whichever is closest to the window
    best = None
    for thr in (2, 3, 4, 5):
        edges = compute_edges(models, thr)
        score = 0 if 150 <= len(edges) <= 400 else min(abs(len(edges) - 150), abs(len(edges) - 400))
        if best is None or score < best[0]:
            best = (score, thr, edges)
    return best[1], best[2]


def sanitize_node_id(mid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", mid)


def mermaid_render(models_by_id: dict[str, dict], edges: list[tuple[str, str, int]], title: str) -> str:
    lines = [f"%% {title}", "graph LR"]
    used = set()
    for a, b, _w in edges:
        used.add(a)
        used.add(b)
    # node definitions (sorted for determinism)
    for mid in sorted(used):
        m = models_by_id[mid]
        nid = sanitize_node_id(mid)
        label = m["name"].replace('"', "'")
        lines.append(f'    {nid}["{label}"]:::c_{sanitize_node_id(m["category"])[:20]}')
    # edges
    for a, b, _w in edges:
        lines.append(f"    {sanitize_node_id(a)} --- {sanitize_node_id(b)}")
    # classDefs (one per distinct category in use)
    cats_used = {models_by_id[mid]["category"] for mid in used}
    for cat in sorted(cats_used):
        cls = f"c_{sanitize_node_id(cat)[:20]}"
        color = color_for(cat)
        lines.append(f"    classDef {cls} fill:#1f2937,stroke:{color},color:#fff")
    return "\n".join(lines) + "\n"


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    models = load_nodes()
    models_by_id = {m["id"]: m for m in models}

    threshold, edges = auto_tune(models)

    # degree counts
    degree: dict[str, int] = defaultdict(int)
    for a, b, _w in edges:
        degree[a] += 1
        degree[b] += 1

    # JSON artifact
    nodes_json = [
        {
            "id": m["id"],
            "slug": m["slug"],
            "name": m["name"],
            "category": m["category"],
            "color": color_for(m["category"]),
            "degree": degree.get(m["id"], 0),
        }
        for m in models
    ]
    edges_json = [{"source": a, "target": b, "weight": w} for a, b, w in edges]
    payload = {
        "version": 1,
        "threshold_shared_keywords": threshold,
        "node_count": len(nodes_json),
        "edge_count": len(edges_json),
        "nodes": nodes_json,
        "edges": edges_json,
    }
    (DOCS / "latticework.json").write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n"
    )

    # Full mermaid
    (DOCS / "latticework.mmd").write_text(
        mermaid_render(models_by_id, edges, f"Full latticework (threshold={threshold})")
    )

    # Core subgraph: top 15 hubs + edges among them
    top_hubs = sorted(degree.items(), key=lambda kv: (-kv[1], kv[0]))[:15]
    hub_ids = {mid for mid, _ in top_hubs}
    core_edges = [(a, b, w) for a, b, w in edges if a in hub_ids and b in hub_ids]
    (DOCS / "latticework_core.mmd").write_text(
        mermaid_render(models_by_id, core_edges, "Latticework core (top 15 hubs)")
    )

    # Stats
    avg_deg = (2 * len(edges) / len(models)) if models else 0.0
    print(f"threshold (shared keywords) : {threshold}")
    print(f"nodes                       : {len(models)}")
    print(f"edges                       : {len(edges)}")
    print(f"avg degree                  : {avg_deg:.2f}")
    print("top 5 hubs:")
    for mid, deg in sorted(degree.items(), key=lambda kv: (-kv[1], kv[0]))[:5]:
        m = models_by_id[mid]
        print(f"  {mid} {m['name']:<32} degree={deg}  [{m['category']}]")
    print(f"core subgraph edges         : {len(core_edges)} (across {len(hub_ids)} hub nodes)")


if __name__ == "__main__":
    main()
