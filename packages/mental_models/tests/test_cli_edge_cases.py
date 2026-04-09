"""Edge-case tests for the mental-models CLI and selector.

These exist as a regression net for the v0.2.0 polish pass: input validation,
exit codes, JSON-on-stdout guarantees, tokenizer edge cases, and apply schema
stability.
"""
from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from mental_models import load_index, select_models
from mental_models.cli import main as cli_main
from mental_models.selector import _tokenize


def run_cli(argv: list[str]) -> tuple[int, str, str]:
    """Run the CLI and capture (rc, stdout, stderr)."""
    out = io.StringIO()
    err = io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            rc = cli_main(argv)
        except SystemExit as e:  # argparse errors
            rc = int(e.code) if e.code is not None else 0
    return rc, out.getvalue(), err.getvalue()


class TestTokenizerEdgeCases(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(_tokenize(""), [])

    def test_none_safe(self):
        self.assertEqual(_tokenize(None), [])  # type: ignore[arg-type]

    def test_only_stopwords(self):
        self.assertEqual(_tokenize("the is a an and"), [])

    def test_apostrophes(self):
        # Apostrophes split words; content pieces survive if non-stopword.
        toks = _tokenize("can't it's well-being")
        self.assertIn("well-being", toks)
        self.assertIn("well", toks)

    def test_numbers_do_not_crash(self):
        toks = _tokenize("80/20 rule and 10x growth")
        self.assertIn("rule", toks)
        self.assertIn("growth", toks)

    def test_unicode_ignored(self):
        # Current limitation: tokenizer is ASCII-only; unicode letters get
        # chopped out but the tokenizer must not crash.
        toks = _tokenize("café naïve résumé")
        self.assertIsInstance(toks, list)

    def test_very_long_input_truncated(self):
        toks = _tokenize("inversion " * 5000)  # ~55KB
        self.assertIn("inversion", toks)
        # Upper bound: ~4096 chars / 10 chars per token => a few hundred tokens.
        self.assertLess(len(toks), 1000)


class TestSelectorEdgeCases(unittest.TestCase):
    def test_empty_query(self):
        self.assertEqual(select_models(""), [])

    def test_stopwords_only(self):
        self.assertEqual(select_models("the is a"), [])

    def test_unicode_emoji(self):
        # Should not raise; may or may not return results.
        results = select_models("inversion 🔄 thinking", top_k=3)
        self.assertIsInstance(results, list)

    def test_negative_top_k(self):
        self.assertEqual(select_models("inversion", top_k=-1), [])

    def test_zero_top_k(self):
        self.assertEqual(select_models("inversion", top_k=0), [])

    def test_10kb_query(self):
        q = "inversion probability risk " * 500
        results = select_models(q, top_k=5)
        self.assertGreater(len(results), 0)


class TestCliEdgeCases(unittest.TestCase):
    def test_no_args_prints_help_exit_0(self):
        rc, out, err = run_cli([])
        self.assertEqual(rc, 0)
        self.assertIn("mental-models", out.lower())

    def test_version_flag(self):
        rc, out, _ = run_cli(["--version"])
        self.assertEqual(rc, 0)
        self.assertTrue(out.strip())
        # Looks like a version string
        self.assertRegex(out.strip(), r"^\d+\.\d+")

    def test_short_version_flag(self):
        rc, out, _ = run_cli(["-V"])
        self.assertEqual(rc, 0)
        self.assertTrue(out.strip())

    def test_unknown_subcommand_exit_2(self):
        rc, _, err = run_cli(["does-not-exist"])
        self.assertEqual(rc, 2)

    def test_select_stopwords_only_exit_2(self):
        rc, out, err = run_cli(["select", "the", "is", "a"])
        self.assertEqual(rc, 2)
        self.assertIn("stopwords", err.lower() + out.lower())

    def test_select_stopwords_only_json_stdout_is_valid(self):
        rc, out, err = run_cli(["select", "--json", "the", "is", "a"])
        self.assertEqual(rc, 2)
        data = json.loads(out)  # must be valid JSON
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["models"], [])
        # Warning/error must be on stderr, not stdout
        self.assertTrue(err.strip())

    def test_select_unicode_query_no_crash(self):
        rc, out, err = run_cli(["select", "--json", "inversion", "🔄"])
        self.assertEqual(rc, 0)
        json.loads(out)

    def test_select_very_long_query(self):
        long_q = "inversion " * 1500  # ~15KB
        rc, out, err = run_cli(["select", "--json", long_q.strip()])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertGreater(len(data["models"]), 0)
        # Warning on stderr about truncation
        self.assertIn("truncated", err.lower())

    def test_select_negative_top_exit_3(self):
        rc, _, err = run_cli(["select", "inversion", "-k", "-1"])
        self.assertEqual(rc, 3)

    def test_get_case_variations(self):
        for slug in ("INVERSION", "Inversion", "inversion", "  inversion  "):
            rc, out, _ = run_cli(["get", slug, "--field", "slug"])
            self.assertEqual(rc, 0, f"slug={slug!r}")
            self.assertEqual(out.strip(), "inversion")

    def test_get_markdown_ends_with_newline(self):
        rc, out, _ = run_cli(["get", "inversion"])
        self.assertEqual(rc, 0)
        self.assertTrue(out)
        self.assertTrue(out.endswith("\n"))

    def test_apply_no_problem_flag(self):
        rc, out, _ = run_cli(["apply", "inversion", "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(data["problem"], "")
        for key in ("description", "thinking_steps", "coaching_questions", "when_to_avoid"):
            self.assertIn(key, data)

    def test_apply_json_has_all_four_keys_even_when_sections_missing(self):
        """Simulate a model file with no sections by monkey-patching the
        markdown reader to return only a description body."""
        from mental_models import cli as cli_mod
        with patch.object(cli_mod, "_read_model_markdown", return_value=""):
            rc, out, _ = run_cli(["apply", "inversion", "--json"])
            self.assertEqual(rc, 0)
            data = json.loads(out)
            for key in ("description", "thinking_steps", "coaching_questions", "when_to_avoid"):
                self.assertIn(key, data)
            # Missing sections default to empty string, not None
            self.assertEqual(data["thinking_steps"], "")
            self.assertEqual(data["when_to_avoid"], "")

    def test_list_category_exact_case_insensitive(self):
        from mental_models import list_categories
        cats = list_categories()
        self.assertTrue(cats)
        # A real category, upper-cased, still matches
        rc, out, _ = run_cli(["list", "--category", cats[0].upper(), "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertGreater(data["count"], 0)

    def test_list_category_unknown_exit_0_empty(self):
        rc, out, _ = run_cli(["list", "--category", "no-such-category", "--json"])
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["models"], [])

    def test_select_json_valid_for_various_shapes(self):
        queries = [
            ["inversion"],
            ["how", "do", "I", "decide"],
            ["margin", "of", "safety"],
            ["first", "principles", "thinking"],
            ["a", "b", "c", "d", "e", "f"],
        ]
        for q in queries:
            rc, out, _ = run_cli(["select", "--json"] + q)
            self.assertIn(rc, (0, 2), f"rc={rc} q={q}")
            data = json.loads(out)  # must parse
            self.assertIn("models", data)
            self.assertIn("count", data)

    def test_get_not_found_json_stdout_clean(self):
        rc, out, err = run_cli(["get", "no-such-slug"])
        self.assertEqual(rc, 2)
        self.assertIn("no model", err.lower())

    def test_doctor_ok(self):
        rc, out, _ = run_cli(["doctor", "--json"])
        self.assertEqual(rc, 0)
        d = json.loads(out)
        self.assertTrue(d["ok"])

    def test_doctor_missing_index_graceful(self):
        """When the index cannot be resolved, doctor reports ok=False, doesn't
        crash, and still emits valid JSON."""
        from mental_models import cli as cli_mod
        from mental_models import index as index_mod

        # Clear the lru_cache so our patched resolver actually gets called.
        index_mod.load_index.cache_clear()

        def boom() -> object:  # pragma: no cover - raises
            raise FileNotFoundError("simulated: no index")

        with patch.object(cli_mod, "_resolve_index_path", side_effect=boom), \
             patch.object(index_mod, "_resolve_index_path", side_effect=boom):
            rc, out, _ = run_cli(["doctor", "--json"])
            d = json.loads(out)
            self.assertFalse(d["ok"])
            self.assertEqual(rc, 1)

        # Re-populate cache for subsequent tests.
        index_mod.load_index.cache_clear()
        load_index()


if __name__ == "__main__":
    unittest.main()
