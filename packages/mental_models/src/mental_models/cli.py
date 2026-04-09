"""mental-models CLI — the canonical interface for skills, MCP, and humans.

Subcommands:
    select    Select top-k models for a query
    get       Print a model by slug (markdown or structured)
    list      List models, optionally filtered by category
    categories  List all categories
    apply     Return a structured application of a model to a problem
    which     Print the resolved model-index.json path
    doctor    Diagnose install and data resolution
    version   Print the package version

All commands support --json for machine consumers.
Exit codes: 0 ok, 2 not found, 3 bad args, 1 other error.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from . import __version__
from .index import Model, get_model, list_categories, load_index
from .index import _resolve_index_path  # type: ignore[attr-defined]
from .selector import select_models


# ---------- helpers ----------


def _model_to_dict(m: Model) -> dict[str, Any]:
    return {
        "slug": m.slug,
        "name": m.name,
        "category": m.category,
        "keywords": list(m.keywords),
        "description": m.description,
        "path": m.path,
        "id": m.id,
    }


def _read_model_markdown(m: Model) -> str:
    """Best-effort: read the model's full markdown file from disk."""
    if not m.path:
        return ""
    # path is relative to the skill dir; resolve against the index location
    try:
        index_path = _resolve_index_path()
        skill_dir = index_path.parent.parent  # .../mental-models/
        candidate = (skill_dir / m.path).resolve()
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    except Exception:
        pass
    return ""


def _print_json(obj: Any) -> None:
    json.dump(obj, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


# ---------- subcommand handlers ----------


def cmd_select(args: argparse.Namespace) -> int:
    query = " ".join(args.query).strip()
    if not query:
        print("error: empty query", file=sys.stderr)
        return 3
    results = select_models(query, top_k=args.top)
    if args.json:
        _print_json({
            "query": query,
            "count": len(results),
            "models": [_model_to_dict(m) for m in results],
        })
        return 0 if results else 2
    if not results:
        print("No matching models found.", file=sys.stderr)
        return 2
    print(f"Top {len(results)} mental models for: {query!r}\n")
    for i, m in enumerate(results, 1):
        desc = (m.description or "").strip().replace("\n", " ")
        if len(desc) > 140:
            desc = desc[:137] + "..."
        print(f"{i}. {m.name} [{m.slug}]  ({m.category})")
        if desc:
            print(f"   {desc}")
        print(f"   path: {m.path}")
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    try:
        m = get_model(args.slug)
    except KeyError:
        print(f"error: no model with slug {args.slug!r}", file=sys.stderr)
        return 2
    if args.field:
        data = _model_to_dict(m)
        if args.field not in data:
            print(f"error: unknown field {args.field!r}", file=sys.stderr)
            return 3
        val = data[args.field]
        if args.json:
            _print_json(val)
        else:
            print(val if not isinstance(val, list) else "\n".join(val))
        return 0
    if args.json:
        out = _model_to_dict(m)
        out["markdown"] = _read_model_markdown(m)
        _print_json(out)
        return 0
    md = _read_model_markdown(m)
    if md:
        sys.stdout.write(md)
        if not md.endswith("\n"):
            sys.stdout.write("\n")
    else:
        # Fallback: print structured summary
        print(f"# {m.name} [{m.slug}]")
        print(f"Category: {m.category}")
        print(f"Keywords: {', '.join(m.keywords)}")
        print()
        print(m.description)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    models = load_index()
    if args.category:
        models = [m for m in models if m.category.lower() == args.category.lower()]
    if args.json:
        _print_json({
            "count": len(models),
            "models": [_model_to_dict(m) for m in models],
        })
        return 0
    for m in models:
        print(f"{m.slug}\t{m.name}\t{m.category}")
    return 0


def cmd_categories(args: argparse.Namespace) -> int:
    cats = list_categories()
    if args.json:
        _print_json(cats)
    else:
        for c in cats:
            print(c)
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    try:
        m = get_model(args.slug)
    except KeyError:
        print(f"error: no model with slug {args.slug!r}", file=sys.stderr)
        return 2
    problem = " ".join(args.problem).strip() if args.problem else ""
    md = _read_model_markdown(m)
    # Parse the bold-label sections from the markdown
    sections = _extract_sections(md)
    payload = {
        "slug": m.slug,
        "name": m.name,
        "category": m.category,
        "problem": problem,
        "description": sections.get("description") or m.description,
        "thinking_steps": sections.get("thinking steps", ""),
        "coaching_questions": sections.get("coaching questions", ""),
        "when_to_avoid": sections.get("when to avoid", ""),
        "path": m.path,
    }
    if args.json:
        _print_json(payload)
        return 0
    print(f"# Applying {m.name} to: {problem or '(no problem supplied)'}")
    print()
    for key in ("description", "thinking_steps", "coaching_questions", "when_to_avoid"):
        label = key.replace("_", " ").title()
        val = payload[key]
        if val:
            print(f"## {label}\n{val}\n")
    return 0


def _extract_sections(md: str) -> dict[str, str]:
    """Extract canonical top-level sections from a model file.

    Only the 5 canonical labels act as section boundaries. Sub-headings
    inside a section (e.g. **Clearly Define Your Goal:**) stay as body.
    """
    import re
    if not md:
        return {}
    canonical = [
        ("description", re.compile(r"\*\*Description:\*\*", re.IGNORECASE)),
        ("keywords", re.compile(r"\*\*Keywords[^*]*:\*\*", re.IGNORECASE)),
        ("thinking steps", re.compile(r"\*\*Thinking Steps:\*\*", re.IGNORECASE)),
        ("coaching questions", re.compile(r"\*\*Coaching Questions:\*\*", re.IGNORECASE)),
        ("when to avoid", re.compile(r"\*\*When to Avoid[^*]*:\*\*", re.IGNORECASE)),
    ]
    hits: list[tuple[str, int, int]] = []  # (key, start_after_label, label_start)
    for key, pat in canonical:
        m = pat.search(md)
        if m:
            hits.append((key, m.end(), m.start()))
    hits.sort(key=lambda h: h[2])
    sections: dict[str, str] = {}
    for i, (key, body_start, _) in enumerate(hits):
        body_end = hits[i + 1][2] if i + 1 < len(hits) else len(md)
        sections[key] = md[body_start:body_end].strip()
    return sections


def cmd_which(args: argparse.Namespace) -> int:
    try:
        p = _resolve_index_path()
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if args.json:
        _print_json({"path": str(p), "exists": p.is_file()})
    else:
        print(p)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    report: dict[str, Any] = {"version": __version__, "ok": True, "checks": {}}
    try:
        path = _resolve_index_path()
        report["checks"]["index_path"] = str(path)
        report["checks"]["index_exists"] = path.is_file()
    except Exception as e:
        report["ok"] = False
        report["checks"]["index_error"] = str(e)
    try:
        models = load_index()
        report["checks"]["model_count"] = len(models)
        if len(models) < 1:
            report["ok"] = False
    except Exception as e:
        report["ok"] = False
        report["checks"]["load_error"] = str(e)
    try:
        cats = list_categories()
        report["checks"]["category_count"] = len(cats)
    except Exception as e:
        report["ok"] = False
        report["checks"]["categories_error"] = str(e)

    if args.json:
        _print_json(report)
    else:
        print(f"mental-models {report['version']}")
        print(f"status: {'OK' if report['ok'] else 'FAIL'}")
        for k, v in report["checks"].items():
            print(f"  {k}: {v}")
    return 0 if report["ok"] else 1


def cmd_version(args: argparse.Namespace) -> int:
    if args.json:
        _print_json({"version": __version__})
    else:
        print(__version__)
    return 0


# ---------- argparse plumbing ----------


def _build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="Emit JSON output (machine-readable)")

    parser = argparse.ArgumentParser(
        prog="mental-models",
        description="Charlie Munger's latticework of mental models — CLI.",
        parents=[common],
    )
    parser.add_argument("-V", "--version", action="store_true", help="Print version and exit")

    sub = parser.add_subparsers(dest="cmd", metavar="<command>")

    def add(name: str, **kw: Any) -> argparse.ArgumentParser:
        return sub.add_parser(name, parents=[common], **kw)

    p_select = add("select", help="Select top-k models for a query")
    p_select.add_argument("query", nargs="+", help="Problem or question")
    p_select.add_argument("-k", "--top", type=int, default=5, help="Number of models to return")
    p_select.set_defaults(func=cmd_select)

    p_get = add("get", help="Get a model by slug")
    p_get.add_argument("slug", help="Model slug (e.g. inversion)")
    p_get.add_argument("--field", help="Return a single field (name, description, keywords, ...)")
    p_get.set_defaults(func=cmd_get)

    p_list = add("list", help="List models")
    p_list.add_argument("--category", help="Filter by category")
    p_list.set_defaults(func=cmd_list)

    p_cats = add("categories", help="List all categories")
    p_cats.set_defaults(func=cmd_categories)

    p_apply = add("apply", help="Apply a model to a problem (structured output)")
    p_apply.add_argument("slug", help="Model slug")
    p_apply.add_argument("--problem", nargs="*", help="The problem to apply the model to")
    p_apply.set_defaults(func=cmd_apply)

    p_which = add("which", help="Print the resolved model-index.json path")
    p_which.set_defaults(func=cmd_which)

    p_doctor = add("doctor", help="Diagnose install and data resolution")
    p_doctor.set_defaults(func=cmd_doctor)

    p_ver = add("version", help="Print version")
    p_ver.set_defaults(func=cmd_version)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    if not args.cmd:
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
