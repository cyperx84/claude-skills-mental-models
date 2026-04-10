"""Public utilities for serializing, reading, and parsing mental models.

These were previously private helpers duplicated across the CLI and MCP server.
Now they live here as the single source of truth.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .index import Model, _resolve_index_path


def model_to_dict(m: Model) -> dict[str, Any]:
    """Serialize a ``Model`` to a plain dict suitable for JSON output."""
    return {
        "slug": m.slug,
        "name": m.name,
        "category": m.category,
        "keywords": list(m.keywords),
        "description": m.description,
        "path": m.path,
        "id": m.id,
    }


def read_model_markdown(m: Model) -> str:
    """Best-effort: read the model's full markdown file from disk.

    The ``path`` field on each model is relative to the skill directory.
    We resolve it against the index location.
    """
    if not m.path:
        return ""
    try:
        index_path = _resolve_index_path()
        skill_dir = index_path.parent.parent  # .../mental-models/
        candidate = (skill_dir / m.path).resolve()
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    except Exception:
        pass
    return ""


def extract_sections(md: str) -> dict[str, str]:
    """Extract canonical top-level sections from a model file.

    Only the 5 canonical labels act as section boundaries.  Sub-headings
    inside a section (e.g. **Clearly Define Your Goal:**) stay as body.

    Returns a dict keyed by lowercase section name (e.g. ``"thinking steps"``).
    """
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
        match = pat.search(md)
        if match:
            hits.append((key, match.end(), match.start()))
    hits.sort(key=lambda h: h[2])
    sections: dict[str, str] = {}
    for i, (key, body_start, _) in enumerate(hits):
        body_end = hits[i + 1][2] if i + 1 < len(hits) else len(md)
        sections[key] = md[body_start:body_end].strip()
    return sections
