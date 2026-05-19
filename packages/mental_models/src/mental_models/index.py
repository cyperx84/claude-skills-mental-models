"""Load the mental models index and provide basic lookups.

Index resolution strategy:
1. Walk up from the current working directory looking for the repo's canonical
   ``.claude/skills/mental-models/resources/model-index.json``. This keeps an
   editable/dev install aligned with repo edits.
2. Fall back to the bundled copy at ``mental_models/data/model-index.json``
   (which in the source tree is a symlink to the canonical file, but becomes a
   real file when the wheel is built).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Model:
    slug: str
    name: str
    category: str
    keywords: tuple[str, ...]
    description: str
    path: str
    id: str = ""
    thinking_steps: str = ""
    coaching_questions: str = ""
    when_to_avoid: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Model":
        return cls(
            slug=d["slug"],
            name=d["name"],
            category=d.get("category", ""),
            keywords=tuple(d.get("keywords", []) or []),
            description=d.get("summary", "") or d.get("description", ""),
            path=d.get("path", ""),
            id=d.get("id", ""),
            thinking_steps=d.get("thinking_steps", ""),
            coaching_questions=d.get("coaching_questions", ""),
            when_to_avoid=d.get("when_to_avoid", ""),
        )


def _candidate_paths() -> Iterable[Path]:
    # 1. Walk up from cwd looking for the repo copy
    cwd = Path.cwd().resolve()
    for parent in [cwd, *cwd.parents]:
        candidate = parent / ".claude" / "skills" / "mental-models" / "resources" / "model-index.json"
        if candidate.is_file():
            yield candidate
            break
    # 2. Walk up from this file (useful for editable installs inside the repo)
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / ".claude" / "skills" / "mental-models" / "resources" / "model-index.json"
        if candidate.is_file():
            yield candidate
            break
    # 3. Bundled package data fallback
    yield Path(__file__).resolve().parent / "data" / "model-index.json"


def _resolve_index_path() -> Path:
    for p in _candidate_paths():
        if p.is_file():
            return p
    raise FileNotFoundError("Could not locate model-index.json")


@lru_cache(maxsize=1)
def load_index() -> list[Model]:
    """Load and cache all models from the index JSON."""
    path = _resolve_index_path()
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [Model.from_dict(m) for m in data.get("models", [])]


def get_model(slug: str) -> Model:
    """Look up a model by slug. Raises KeyError if not found."""
    slug_norm = slug.strip().lower()
    for m in load_index():
        if m.slug.lower() == slug_norm:
            return m
    raise KeyError(f"No model with slug: {slug!r}")


def list_categories() -> list[str]:
    """Return sorted unique category names."""
    return sorted({m.category for m in load_index() if m.category})
