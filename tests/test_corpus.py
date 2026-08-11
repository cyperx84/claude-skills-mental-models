"""Contracts for the corpus loader -- the single markdown parser."""

from __future__ import annotations

import pytest

from mental_models_kit import (
    CATEGORIES,
    ModelNotFound,
    get_model,
    list_categories,
    list_models,
    load_models,
    normalize_slug,
    set_content_root,
)
from mental_models_kit.corpus import UnknownCategory, parse_markdown, resolve_category

SECTIONS = ("description", "when_to_avoid", "keywords", "thinking_steps", "coaching_questions")


def test_exactly_98_models_load():
    assert len(load_models()) == 98


def test_template_is_excluded_by_filename():
    assert all(m.slug != "_TEMPLATE" for m in load_models())
    assert not any(m.path.endswith("_TEMPLATE.md") for m in load_models())


def test_every_model_has_every_section_populated():
    """Report every offender, not just the first."""
    missing = [
        f"{m.path}:{name}"
        for m in load_models()
        for name in ("description", "when_to_avoid", "thinking_steps", "coaching_questions")
        if not getattr(m, name).strip()
    ]
    missing += [m.path for m in load_models() if not m.keywords]
    assert missing == []


def test_every_model_has_name_and_category_detail():
    bad = [m.path for m in load_models() if not m.name or not m.category_detail]
    assert bad == []


def test_eight_categories_with_the_canonical_counts():
    cats = list_categories()
    assert [c.key for c in cats] == [key for key, _d, _dir, _n in CATEGORIES]
    assert [c.count for c in cats] == [n for _k, _d, _dir, n in CATEGORIES]
    assert sum(c.count for c in cats) == 98


def test_category_comes_from_the_directory_not_the_category_line():
    """The five War models carry five different `**Category = Warfare & X**`
    strings. Trusting that line yields 12 categories and makes filtering silently
    return nothing."""
    war = list_models("war")
    assert len(war) == 5
    assert {m.category for m in war} == {"Warfare & Strategy"}
    assert len({m.category_detail for m in war}) == 5


def test_normalized_slugs_are_unique():
    normed = [normalize_slug(m.slug) for m in load_models()]
    assert len(set(normed)) == 98, "slug normalization collides"


def test_ids_are_unique():
    ids = [m.id for m in load_models()]
    assert len(set(ids)) == 98


def test_models_sorted_by_category_order_then_id():
    order = {key: i for i, (key, _d, _dir, _n) in enumerate(CATEGORIES)}
    keys = [(order[m.category_key], m.id) for m in load_models()]
    assert keys == sorted(keys)


@pytest.mark.parametrize(
    "key", ["inversion", "INVERSION", "  inversion  ", "m07", "M07", "Inversion"]
)
def test_get_model_lookup_is_tolerant(key):
    assert get_model(key).slug == "inversion"


@pytest.mark.parametrize("key", ["hanlon's_razor", "hanlons-razor", "Hanlons Razor"])
def test_apostrophe_slug_resolves_three_ways(key):
    """Named case: the apostrophe slugs must not need exact byte spelling."""
    assert get_model(key).slug == "hanlon's_razor"


def test_get_model_unknown_raises():
    with pytest.raises(ModelNotFound):
        get_model("nope")


def test_get_model_empty_raises():
    with pytest.raises(ModelNotFound):
        get_model("   ")


def test_descriptions_are_never_truncated():
    """The old JSON index stored `Description[:200] + "..."` for all 98 models.
    Nothing may reintroduce that."""
    models = load_models()
    assert not any(m.description.endswith("...") for m in models)
    assert any(len(m.description) > 203 for m in models)


def test_markdown_is_the_whole_file():
    m = get_model("inversion")
    assert m.markdown.lstrip().startswith("## Mental Model =")
    assert m.thinking_steps in m.markdown
    assert m.coaching_questions in m.markdown


def test_parser_is_order_independent():
    text = (
        "## Mental Model = Reordered\n\n"
        "**Category = Art**\n"
        "**Coaching Questions:**\nQ\n\n"
        "**Thinking Steps:**\nS\n\n"
        "**Keywords for Situations:**\nk1, k2.\n\n"
        "**When to Avoid (or Use with Caution):**\nA\n\n"
        "**Description:**\nD\n"
    )
    parsed = parse_markdown(text)
    assert parsed["name"] == "Reordered"
    assert parsed["category_detail"] == "Art"
    assert [parsed[s] for s in SECTIONS] == ["D", "A", "k1, k2.", "S", "Q"]


def test_sub_bold_headings_are_body_not_boundaries():
    m = get_model("inversion")
    assert "**Clearly Define Your Goal:**" in m.thinking_steps


def test_resolve_category_accepts_key_and_display_and_is_tolerant():
    for value in ("human-nature", "Human Nature & Judgment", "  HUMAN NATURE & JUDGMENT "):
        assert resolve_category(value).key == "human-nature"


def test_resolve_category_rejects_unknown_with_the_valid_keys():
    with pytest.raises(UnknownCategory) as excinfo:
        resolve_category("Strategy")
    for key, _d, _dir, _n in CATEGORIES:
        assert key in str(excinfo.value)


def test_set_content_root_isolates_state(fixture_root):
    models = load_models()
    assert len(models) == 2
    assert [m.slug for m in models] == ["alpha_thing", "beta's_thing"]
    assert get_model("betas-thing").name == "Beta's Thing"
    assert [c.count for c in list_categories()] == [1, 0, 0, 0, 0, 0, 1, 0]


def test_content_root_restores_after_override(fixture_root):
    set_content_root(None)
    assert len(load_models()) == 98
