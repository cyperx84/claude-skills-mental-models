"""Contracts for the compact catalog -- the primary selection surface."""

from __future__ import annotations

import pytest

from mental_models_kit import list_categories, load_models, render_catalog, skill_root
from mental_models_kit.catalog import catalog_document
from mental_models_kit.corpus import UnknownCategory, clear_caches


def test_compact_catalog_contains_every_slug():
    text = render_catalog("compact")
    missing = [m.slug for m in load_models() if f"`{m.slug}`" not in text]
    assert missing == []


def test_catalog_contains_every_category_heading_with_its_count():
    text = render_catalog("compact")
    for c in list_categories():
        assert f"## {c.display} ({c.count})" in text


def test_compact_carries_keywords_and_slim_does_not():
    m = load_models()[0]
    assert m.keywords[0] in render_catalog("compact")
    slim = render_catalog("slim")
    assert f"`{m.slug}` — {m.name}\n" in slim


def test_token_budget_ceilings():
    """~4.3k tokens compact / ~1.5k slim. These are hard ceilings, not targets."""
    assert len(render_catalog("compact").encode("utf-8")) < 20_000
    assert len(render_catalog("slim").encode("utf-8")) < 8_000


def test_catalog_is_byte_stable_across_calls_and_cache_clears():
    first = catalog_document("compact")
    second = catalog_document("compact")
    clear_caches()
    third = catalog_document("compact")
    assert first == second == third


def test_catalog_ends_with_exactly_one_newline_and_no_trailing_whitespace():
    doc = catalog_document("compact")
    assert doc.endswith("\n") and not doc.endswith("\n\n")
    assert all(line == line.rstrip() for line in doc.split("\n"))


def test_category_filter_narrows_the_catalog():
    war = render_catalog("compact", category="war")
    assert "## Warfare & Strategy (5)" in war
    assert "## Economics" not in war


def test_unknown_format_and_category_raise():
    with pytest.raises(ValueError):
        render_catalog("fancy")
    with pytest.raises(UnknownCategory):
        render_catalog("compact", category="Strategy")


def test_committed_catalog_md_matches_generated_bytes():
    """The CI drift gate in one assertion: `mental-models catalog --with-header`
    must reproduce skills/mental-models/CATALOG.md byte for byte."""
    committed = skill_root() / "CATALOG.md"
    if not committed.is_file():
        pytest.skip(f"no committed CATALOG.md at {committed}")
    assert committed.read_bytes() == catalog_document("compact").encode("utf-8")
