"""Unit tests for MCP tool handlers (in-process, no transport)."""
import unittest

from mental_models_mcp.server import (
    mm_apply,
    mm_categories,
    mm_compare,
    mm_doctor,
    mm_get,
    mm_list,
    mm_random,
    mm_select,
)


class TestTools(unittest.TestCase):
    def test_mm_select_returns_models(self):
        out = mm_select("how do I decide between two jobs", top_k=5)
        self.assertNotIn("error", out)
        self.assertIn("models", out)
        self.assertGreater(out["count"], 0)
        self.assertLessEqual(len(out["models"]), 5)
        self.assertIn("slug", out["models"][0])

    def test_mm_select_empty_query(self):
        out = mm_select("", top_k=5)
        self.assertEqual(out["count"], 0)
        self.assertEqual(out["models"], [])

    def test_mm_get_full(self):
        out = mm_get("inversion")
        self.assertNotIn("error", out)
        self.assertEqual(out["slug"], "inversion")
        self.assertIn("markdown", out)
        self.assertIn("name", out)

    def test_mm_get_field(self):
        out = mm_get("inversion", field="name")
        self.assertEqual(out["field"], "name")
        self.assertIn("Inversion", out["value"])

    def test_mm_get_not_found(self):
        out = mm_get("not_a_real_slug_xyz")
        self.assertIn("error", out)

    def test_mm_list(self):
        out = mm_list()
        self.assertGreaterEqual(out["count"], 90)
        self.assertEqual(out["count"], len(out["models"]))

    def test_mm_list_filtered(self):
        cats = mm_categories()["categories"]
        self.assertGreater(len(cats), 0)
        out = mm_list(category=cats[0])
        self.assertGreater(out["count"], 0)
        for m in out["models"]:
            self.assertEqual(m["category"].lower(), cats[0].lower())

    def test_mm_categories(self):
        out = mm_categories()
        self.assertIn("categories", out)
        self.assertGreater(out["count"], 0)

    def test_mm_apply_has_sections(self):
        out = mm_apply("inversion", "pricing strategy")
        self.assertNotIn("error", out)
        self.assertEqual(out["slug"], "inversion")
        self.assertGreater(len(out["thinking_steps"]), 100)
        self.assertGreater(len(out["when_to_avoid"]), 50)

    def test_mm_apply_not_found(self):
        out = mm_apply("not_a_real_slug_xyz", "problem")
        self.assertIn("error", out)

    def test_mm_compare_two_models(self):
        out = mm_compare(["inversion", "bottlenecks"])
        self.assertNotIn("error", out)
        self.assertEqual(len(out["models"]), 2)
        self.assertIn("shared_keywords", out)
        self.assertIn("unique_keywords", out)
        self.assertGreater(out["categories_spanned"], 0)

    def test_mm_compare_unknown_slug(self):
        out = mm_compare(["inversion", "not_a_real_slug_xyz"])
        self.assertIn("error", out)

    def test_mm_compare_too_few(self):
        out = mm_compare(["inversion"])
        self.assertIn("error", out)

    def test_mm_random_returns_model(self):
        out = mm_random()
        self.assertNotIn("error", out)
        self.assertIn("slug", out)
        self.assertIn("name", out)
        self.assertIn("markdown", out)

    def test_mm_random_with_category(self):
        cats = mm_categories()["categories"]
        out = mm_random(category=cats[0])
        self.assertNotIn("error", out)
        self.assertEqual(out["category"].lower(), cats[0].lower())

    def test_mm_random_unknown_category(self):
        out = mm_random(category="no-such-category-xyz")
        self.assertIn("error", out)

    def test_mm_doctor_ok(self):
        out = mm_doctor()
        self.assertTrue(out["ok"])
        self.assertGreaterEqual(out["checks"]["model_count"], 90)


if __name__ == "__main__":
    unittest.main()
