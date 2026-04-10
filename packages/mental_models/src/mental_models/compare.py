"""Compare mental models and discover random models from the latticework."""
from __future__ import annotations

import random as _random
from typing import Any, Optional

from .index import Model, get_model, load_index, list_categories
from .utils import model_to_dict, read_model_markdown, extract_sections


def compare_models(slugs: list[str]) -> dict[str, Any]:
    """Compare 2-3 mental models side by side.

    Returns a dict with per-model summaries, shared/unique keywords, and the
    number of distinct categories spanned (the latticework principle: coverage
    across categories beats depth in one).

    Raises ``KeyError`` if any slug is not found.
    Raises ``ValueError`` if fewer than 2 or more than 3 slugs are given.
    """
    if len(slugs) < 2 or len(slugs) > 3:
        raise ValueError("compare_models requires 2 or 3 slugs")

    models = [get_model(s) for s in slugs]

    # Build per-model keyword sets
    kw_sets: dict[str, set[str]] = {}
    for m in models:
        kw_sets[m.slug] = {k.lower() for k in m.keywords}

    # Shared: keywords appearing in 2+ models
    all_kws: list[str] = []
    for s in kw_sets.values():
        all_kws.extend(s)
    shared = {k for k in set(all_kws) if all_kws.count(k) >= 2}

    # Unique: per-model keywords not in any other model
    unique: dict[str, list[str]] = {}
    for slug, kws in kw_sets.items():
        others = set()
        for other_slug, other_kws in kw_sets.items():
            if other_slug != slug:
                others |= other_kws
        unique[slug] = sorted(kws - others)

    # Per-model structured info
    model_details: list[dict[str, Any]] = []
    for m in models:
        md = read_model_markdown(m)
        sections = extract_sections(md)
        model_details.append({
            **model_to_dict(m),
            "thinking_steps": sections.get("thinking steps", ""),
            "when_to_avoid": sections.get("when to avoid", ""),
        })

    categories_spanned = len({m.category for m in models})

    return {
        "slugs": [m.slug for m in models],
        "models": model_details,
        "shared_keywords": sorted(shared),
        "unique_keywords": unique,
        "categories_spanned": categories_spanned,
    }


def random_model(category: str | None = None) -> Model:
    """Return a random model, optionally filtered by category.

    Raises ``ValueError`` if the category has no models.
    """
    models = load_index()
    if category:
        cat_norm = category.strip().lower()
        models = [m for m in models if m.category.lower() == cat_norm]
    if not models:
        raise ValueError(f"no models found for category: {category!r}")
    return _random.choice(models)
