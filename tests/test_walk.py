"""Contracts for `walk` / split_steps (issue #4).

These assert invariants, not a snapshot of today's text: step counts and exact
prose belong to the corpus and may legitimately change when a model is edited.
"""
from __future__ import annotations

import pytest

from mental_models_kit.corpus import get_model, load_models
from mental_models_kit.render import split_steps, walk_dict


def test_every_model_splits_into_at_least_one_step():
    """The splitter must never return empty for any shipped model."""
    empty = [m.slug for m in load_models() if not split_steps(m.thinking_steps)]
    assert empty == [], f"models whose thinking_steps split to nothing: {empty}"


def test_steps_partition_the_source_text():
    """Splitting must not invent or drop content -- only segment it."""
    for m in load_models():
        joined = "".join(split_steps(m.thinking_steps))
        source = "".join(m.thinking_steps.split())
        assert "".join(joined.split()) == source, f"{m.slug}: split lost or added text"


def test_unnumbered_prose_survives_as_one_step():
    assert split_steps("Just prose, no markers here.") == ["Just prose, no markers here."]


def test_empty_input_yields_no_steps():
    assert split_steps("") == []
    assert split_steps("   \n  ") == []


def test_walk_is_stateless_and_repeatable():
    m = get_model("inversion")
    assert walk_dict(m, 0) == walk_dict(m, 0)


def test_walk_past_the_end_reports_done_not_an_error():
    m = get_model("inversion")
    out = walk_dict(m, 10_000)
    assert out["done"] is True
    assert out["content"] is None
    assert out["total"] == len(split_steps(m.thinking_steps))


def test_walk_advances_until_done_for_every_model():
    """A caller can advance from 0 without knowing the count and always terminate."""
    for m in load_models():
        seen = 0
        while not walk_dict(m, seen)["done"]:
            seen += 1
            assert seen < 100, f"{m.slug}: walk never reported done"
        assert seen == len(split_steps(m.thinking_steps))


def test_problem_is_echoed_only_when_supplied():
    m = get_model("inversion")
    assert "problem" not in walk_dict(m, 0)
    assert walk_dict(m, 0, "should I switch jobs")["problem"] == "should I switch jobs"


@pytest.mark.parametrize("bad", [-1, -99])
def test_negative_steps_are_done_not_a_crash(bad):
    assert walk_dict(get_model("inversion"), bad)["done"] is True
