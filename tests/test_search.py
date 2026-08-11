"""Behaviour contracts for the keyword fallback.

Deliberately asserts nothing about `_stem`/`_tokenize` internals -- the deleted
tests froze eleven hardcoded stem pairs and broke on any tokenizer change with
no user-visible cause.
"""

from __future__ import annotations

import pytest

from mental_models_kit import search_models


def test_exact_model_name_query_ranks_that_model_first():
    """This is retrieval, which is the scorer's real job. It must work."""
    for query, slug in [
        ("inversion", "inversion"),
        ("Circle of Competence", "circle_of_competence"),
        ("margin of safety", "margin_of_safety"),
        ("Occam's Razor", "occam's_razor"),
    ]:
        assert search_models(query, 5)[0].slug == slug, query


def test_top_k_is_respected():
    assert len(search_models("planning risk", 3)) <= 3
    assert len(search_models("planning risk", 1)) == 1


@pytest.mark.parametrize("k", [0, -1, -100])
def test_non_positive_top_k_returns_empty(k):
    assert search_models("inversion", k) == ()


@pytest.mark.parametrize("query", ["", "   ", "the a of and to", "!!! ??? ..."])
def test_unsearchable_queries_return_empty(query):
    assert search_models(query, 5) == ()


def test_results_are_deterministic():
    a = [m.slug for m in search_models("systems feedback growth", 8)]
    b = [m.slug for m in search_models("systems feedback growth", 8)]
    assert a == b


def test_ties_break_on_slug():
    """Two runs cannot disagree, and equal scores must order by slug."""
    from mental_models_kit.search import _score, _tokenize

    results = search_models("planning", 20)
    tokens = _tokenize("planning")
    scored = [(-_score(m, tokens, "planning"), m.slug) for m in results]
    assert scored == sorted(scored)


def test_a_nonsense_token_matches_nothing():
    assert search_models("zzzqqqxxvv", 5) == ()


def test_very_long_query_is_handled_without_error():
    assert isinstance(search_models("inversion " * 5000, 3), tuple)


def test_search_respects_an_overridden_content_root(fixture_root):
    """The token index must not survive a content-root swap."""
    assert [m.slug for m in search_models("alpha", 5)] == ["alpha_thing"]
    assert search_models("inversion", 5) == ()
