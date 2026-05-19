#!/usr/bin/env python3
"""Parse every model markdown file, extract its sections, and compile them into model-index.json.

This eliminates runtime filesystem dependencies and allows the python package
and MCP server to remain 100% self-contained in pure wheel installations.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "mental-models"
INDEX_JSON = SKILL_DIR / "resources" / "model-index.json"


def _extract_sections(md: str) -> dict[str, str]:
    if not md:
        return {}
    canonical = [
        ("description", re.compile(r"\*\*Description:\*\*", re.IGNORECASE)),
        ("keywords", re.compile(r"\*\*Keywords[^*]*:\*\*", re.IGNORECASE)),
        ("thinking steps", re.compile(r"\*\*Thinking Steps:\*\*", re.IGNORECASE)),
        ("coaching questions", re.compile(r"\*\*Coaching Questions:\*\*", re.IGNORECASE)),
        ("when to avoid", re.compile(r"\*\*When to Avoid[^*]*:\*\*", re.IGNORECASE)),
    ]
    hits: list[tuple[str, int, int]] = []
    for key, pat in canonical:
        match = pat.search(md)
        if match:
            hits.append((key, match.end(), match.start()))
    hits.sort(key=lambda h: h[2])
    sections: dict[str, str] = {}
    for i, (key, body_start, _) in enumerate(hits):
        body_end = hits[i + 1][2] if i + 1 < len(hits) else len(md)
        sections[key] = md[body_start:body_end].strip()
    return sections


def main() -> int:
    if not INDEX_JSON.exists():
        print(f"Error: {INDEX_JSON} does not exist.")
        return 1

    with INDEX_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    updated_models = []
    for m in data.get("models", []):
        path_str = m.get("path")
        if not path_str:
            updated_models.append(m)
            continue

        abs_path = (SKILL_DIR / path_str).resolve()
        if not abs_path.is_file():
            print(f"Warning: File {abs_path} not found for slug {m.get('slug')}")
            updated_models.append(m)
            continue

        md = abs_path.read_text(encoding="utf-8")
        sections = _extract_sections(md)

        # Update metadata dictionary
        m["thinking_steps"] = sections.get("thinking steps", "")
        m["coaching_questions"] = sections.get("coaching questions", "")
        m["when_to_avoid"] = sections.get("when to avoid", "")
        updated_models.append(m)

    data["models"] = updated_models

    with INDEX_JSON.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Successfully compiled sections into {INDEX_JSON} for {len(updated_models)} models!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
