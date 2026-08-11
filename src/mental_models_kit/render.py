"""Shared serialisers. The CLI and the MCP server both format through here so
their JSON shapes cannot drift apart."""

from __future__ import annotations

from typing import Any

from .corpus import Model

__all__ = [
    "FIELD_NAMES",
    "apply_dict",
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
