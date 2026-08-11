"""Shared serialisers. The CLI and the MCP server both format through here so
their JSON shapes cannot drift apart."""

from __future__ import annotations

import re
from typing import Any

from .corpus import Model

__all__ = [
    "FIELD_NAMES",
    "apply_dict",
    "split_steps",
    "walk_dict",
    "field_value",
    "model_detail_dict",
    "model_dict",
]

#: ``ModelDict`` -- key order is a tested contract.
_SUMMARY_KEYS = (
    "slug",
    "id",
    "name",
    "category",
    "category_key",
    "keywords",
    "description",
    "path",
)

#: Everything ``get --field`` / ``mm_get(field=...)`` will accept.
FIELD_NAMES: tuple[str, ...] = _SUMMARY_KEYS + (
    "category_detail",
    "when_to_avoid",
    "thinking_steps",
    "coaching_questions",
    "markdown",
)


def model_dict(m: Model) -> dict[str, Any]:
    """The 8-key ``ModelDict``. ``description`` is the full prose, never truncated."""
    return {
        "slug": m.slug,
        "id": m.id,
        "name": m.name,
        "category": m.category,
        "category_key": m.category_key,
        "keywords": list(m.keywords),
        "description": m.description,
        "path": m.path,
    }


def model_detail_dict(m: Model) -> dict[str, Any]:
    """``ModelDict`` plus the raw category string, the four prose sections and
    the complete markdown."""
    out = model_dict(m)
    out["category_detail"] = m.category_detail
    out["when_to_avoid"] = m.when_to_avoid
    out["thinking_steps"] = m.thinking_steps
    out["coaching_questions"] = m.coaching_questions
    out["markdown"] = m.markdown
    return out


def field_value(m: Model, name: str) -> Any:
    """Single-field accessor. Raises ``ValueError`` naming the valid fields."""
    if name not in FIELD_NAMES:
        raise ValueError(
            f"Unknown field {name!r}. Valid fields: {', '.join(FIELD_NAMES)}"
        )
    if name == "keywords":
        return list(m.keywords)
    return getattr(m, name)


def apply_dict(m: Model, problem: str = "") -> dict[str, Any]:
    """Stable scaffold payload. Every key is always present; absent sections are
    ``""`` rather than ``null`` so consumers never branch on type."""
    return {
        "slug": m.slug,
        "id": m.id,
        "name": m.name,
        "category": m.category,
        "category_key": m.category_key,
        "category_detail": m.category_detail,
        "problem": problem or "",
        "description": m.description or "",
        "thinking_steps": m.thinking_steps or "",
        "coaching_questions": m.coaching_questions or "",
        "when_to_avoid": m.when_to_avoid or "",
        "path": m.path,
    }


# --------------------------------------------------------------------------
# Thinking-steps splitting (issue #4, `walk`)
# --------------------------------------------------------------------------

_STEP_SPLIT_RE = re.compile(r"(?m)^(?=\s*\d+[.)]\s+)")


def split_steps(thinking_steps: str) -> list[str]:
    """Split a ``thinking_steps`` block into individual numbered steps.

    Splits on a zero-width lookahead at each leading numbered marker so the
    marker stays attached to its own step. A block with no numbered markers is
    returned as a single step rather than raising -- every one of the 98 models
    must survive this, including any future model that writes prose instead of
    a numbered list.
    """
    text = (thinking_steps or "").strip()
    if not text:
        return []
    return [chunk.strip() for chunk in _STEP_SPLIT_RE.split(text) if chunk.strip()]


def walk_dict(m: Model, step: int, problem: str = "") -> dict[str, Any]:
    """One step of ``m``'s thinking steps, as a stateless record.

    ``step`` is 0-indexed. Past the end returns ``content: None, done: true``
    so a caller can advance until ``done`` without knowing the count up front.
    """
    steps = split_steps(m.thinking_steps)
    total = len(steps)
    done = step >= total or step < 0
    out: dict[str, Any] = {
        "slug": m.slug,
        "name": m.name,
        "step": step,
        "total": total,
        "content": None if done else steps[step],
        "done": done,
    }
    if problem:
        out["problem"] = problem
    return out
