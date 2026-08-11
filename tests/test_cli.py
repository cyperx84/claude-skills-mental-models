"""CLI contracts: exit codes, JSON shapes, and the stdout/stderr split."""

from __future__ import annotations

import json

import pytest

from mental_models_kit import __version__
from mental_models_kit.cli import main
from mental_models_kit.corpus import ContentRootNotFound
from mental_models_kit.render import FIELD_NAMES

MODEL_DICT_KEYS = [
    "slug",
    "id",
    "name",
    "category",
    "category_key",
    "keywords",
    "description",
    "path",
]


def run(capsys, *argv):
    code = main(list(argv))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


# ------------------------------------------------------------------ exit codes


@pytest.mark.parametrize(
    "argv",
    [
        ("categories",),
        ("list",),
        ("list", "--category", "war"),
        ("catalog",),
        ("get", "inversion"),
        ("apply", "inversion"),
        ("search", "inversion"),
        ("which",),
        ("doctor",),
        ("version",),
        (),
        ("--help",),
    ],
)
def test_exit_0_on_success(capsys, argv):
    assert run(capsys, *argv)[0] == 0


def test_exit_1_on_unexpected_internal_error(capsys, monkeypatch):
    import mental_models_kit.cli as cli

    monkeypatch.setattr(cli, "list_categories", lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    code, out, err = run(capsys, "categories")
    assert code == 1
    assert "boom" in err


@pytest.mark.parametrize(
    "argv",
    [
        ("get", "no-such-model"),
        ("apply", "no-such-model"),
        ("search", "zzzqqqxxvv"),
        ("search", "the", "a", "of"),
    ],
)
def test_exit_2_on_not_found(capsys, argv):
    assert run(capsys, *argv)[0] == 2


@pytest.mark.parametrize(
    "argv",
    [
        ("nosuchsubcommand",),          # unknown subcommand -- NOT exit 2
        ("get",),                        # missing required positional
        ("catalog", "--format", "yaml"),  # bad choice
        ("list", "--nosuchflag"),        # unknown flag
        ("get", ""),                     # empty slug
        ("apply", "  "),                 # whitespace slug
        ("search", ""),                  # empty query
        ("search", "inversion", "--top", "0"),
        ("search", "inversion", "--top", "-3"),
        ("get", "inversion", "--field", "nope"),
        ("list", "--category", "bogus"),
        ("catalog", "--category", "Strategy"),
    ],
)
def test_exit_3_on_bad_arguments(capsys, argv):
    assert run(capsys, *argv)[0] == 3


def test_unknown_subcommand_exit_3(capsys):
    """Replaces the old test_unknown_subcommand_exit_2, which froze argparse's
    hardcoded 2 -- colliding with "not found" -- as a contract."""
    assert run(capsys, "definitely-not-a-command")[0] == 3


@pytest.mark.parametrize("argv", [("which",), ("doctor",), ("list",), ("catalog",)])
def test_exit_4_when_content_root_is_missing(capsys, monkeypatch, argv):
    import mental_models_kit.corpus as corpus

    def boom():
        raise ContentRootNotFound("no content anywhere")

    monkeypatch.setattr(corpus, "_resolve_root", boom)
    assert run(capsys, *argv)[0] == 4


# ------------------------------------------------------------------ JSON shapes


@pytest.mark.parametrize(
    "argv",
    [
        ("catalog",),
        ("get", "inversion"),
        ("get", "inversion", "--field", "keywords"),
        ("list",),
        ("categories",),
        ("apply", "inversion", "--problem", "we ship late"),
        ("search", "inversion"),
        ("which",),
        ("doctor",),
        ("version",),
    ],
)
def test_json_mode_stdout_is_parseable(capsys, argv):
    code, out, err = run(capsys, *argv, "--json")
    assert code == 0
    json.loads(out)


@pytest.mark.parametrize(
    "argv",
    [("get", "no-such-model"), ("list", "--category", "bogus"), ("search", "the", "a")],
)
def test_json_mode_error_paths_never_pollute_stdout(capsys, argv):
    """stdout is either empty or valid JSON -- never a bare human message."""
    code, out, err = run(capsys, *argv, "--json")
    assert code != 0
    if out.strip():
        json.loads(out)
    assert err.strip()


def test_global_json_flag_before_subcommand_is_not_clobbered(capsys):
    code, out, _ = run(capsys, "--json", "list", "--category", "war")
    assert code == 0
    assert json.loads(out)["count"] == 5


def test_catalog_json_shape(capsys):
    payload = json.loads(run(capsys, "catalog", "--json")[1])
    assert payload["count"] == 98
    assert [c["key"] for c in payload["categories"]][0] == "general"
    assert sum(c["count"] for c in payload["categories"]) == 98
    model = payload["categories"][0]["models"][0]
    assert list(model.keys()) == MODEL_DICT_KEYS


def test_catalog_format_json_matches_json_flag(capsys):
    a = run(capsys, "catalog", "--format", "json")[1]
    b = run(capsys, "catalog", "--json")[1]
    assert json.loads(a) == json.loads(b)


def test_get_json_shape_and_full_description(capsys):
    payload = json.loads(run(capsys, "get", "inversion", "--json")[1])
    assert list(payload.keys())[:8] == MODEL_DICT_KEYS
    for extra in ("markdown", "category_detail", "when_to_avoid", "thinking_steps",
                  "coaching_questions"):
        assert extra in payload
    assert not payload["description"].endswith("...")
    assert payload["markdown"].lstrip().startswith("## Mental Model =")


def test_get_field_json_emits_a_bare_value(capsys):
    keywords = json.loads(run(capsys, "get", "inversion", "--field", "keywords", "--json")[1])
    assert isinstance(keywords, list)
    name = json.loads(run(capsys, "get", "inversion", "--field", "name", "--json")[1])
    assert name == "Inversion"


def test_get_field_markdown_is_accepted(capsys):
    """The old CLI rejected --field markdown while MCP accepted it."""
    assert "markdown" in FIELD_NAMES
    code, out, _ = run(capsys, "get", "inversion", "--field", "markdown")
    assert code == 0
    assert out.lstrip().startswith("## Mental Model =")


def test_unknown_field_message_lists_the_valid_fields(capsys):
    code, _out, err = run(capsys, "get", "inversion", "--field", "nope")
    assert code == 3
    for field in FIELD_NAMES:
        assert field in err


def test_list_json_shape(capsys):
    payload = json.loads(run(capsys, "list", "--json")[1])
    assert payload["count"] == 98
    assert len(payload["models"]) == 98
    assert list(payload["models"][0].keys()) == MODEL_DICT_KEYS


def test_categories_json_is_objects_not_strings(capsys):
    cats = json.loads(run(capsys, "categories", "--json")[1])
    assert isinstance(cats, list) and len(cats) == 8
    assert set(cats[0]) == {"key", "display", "count"}


def test_category_filter_accepts_key_or_display_name(capsys):
    by_key = json.loads(run(capsys, "list", "--category", "human-nature", "--json")[1])
    by_display = json.loads(
        run(capsys, "list", "--category", "Human Nature & Judgment", "--json")[1]
    )
    assert by_key["count"] == by_display["count"] == 23
    assert by_key == by_display


def test_unknown_category_is_an_error_not_a_silent_empty_list(capsys):
    code, out, err = run(capsys, "list", "--category", "bogus", "--json")
    assert code == 3
    assert not out.strip()
    for key in ("general", "science", "math", "economics", "systems", "art", "war",
                "human-nature"):
        assert key in err


def test_apply_json_always_has_every_key_and_empty_strings(capsys):
    payload = json.loads(run(capsys, "apply", "inversion", "--json")[1])
    expected = {
        "slug", "id", "name", "category", "category_key", "category_detail", "problem",
        "description", "thinking_steps", "coaching_questions", "when_to_avoid", "path",
    }
    assert set(payload) == expected
    assert payload["problem"] == ""
    assert None not in payload.values()


def test_search_json_shape(capsys):
    payload = json.loads(run(capsys, "search", "inversion", "-k", "2", "--json")[1])
    assert payload["query"] == "inversion"
    assert payload["count"] == len(payload["models"]) <= 2


def test_search_stopword_query_still_emits_valid_json_and_exits_2(capsys):
    code, out, err = run(capsys, "search", "the", "a", "of", "--json")
    assert code == 2
    assert json.loads(out) == {"query": "the a of", "count": 0, "models": []}
    assert "searchable tokens" in err


def test_which_json_shape(capsys):
    payload = json.loads(run(capsys, "which", "--json")[1])
    assert set(payload) == {"content_root", "exists", "source", "model_count"}
    assert payload["exists"] is True
    assert payload["source"] in {"override", "bundled", "repo"}
    assert payload["model_count"] == 98


def test_doctor_json_shape(capsys):
    payload = json.loads(run(capsys, "doctor", "--json")[1])
    assert payload["ok"] is True
    assert payload["version"] == __version__
    assert set(payload["checks"]) == {
        "content_root", "content_root_exists", "source", "model_count",
        "category_count", "catalog_bytes",
    }


def test_version_flag_and_subcommand_agree(capsys):
    assert run(capsys, "-V")[1].strip() == __version__
    assert run(capsys, "version")[1].strip() == __version__


# ------------------------------------------------------------ content root flag


def test_content_root_flag_switches_the_corpus(capsys, fixture_root):
    from mental_models_kit import set_content_root

    set_content_root(None)
    code, out, _ = run(capsys, "--content-root", str(fixture_root), "list", "--json")
    assert code == 0
    assert json.loads(out)["count"] == 2


def test_search_text_output_warns_that_it_is_not_selection(capsys):
    code, out, err = run(capsys, "search", "inversion")
    assert code == 0
    assert "catalog" in err.lower()
    assert "inversion" in out
