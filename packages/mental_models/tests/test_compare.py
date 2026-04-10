"""Tests for mental_models.compare — compare_models and random_model."""
import unittest

from mental_models import Model, list_categories
from mental_models.compare import compare_models, random_model


class TestCompareModels(unittest.TestCase):
    def test_compare_two_models(self):
        result = compare_models(["inversion", "bottlenecks"])
        self.assertEqual(len(result["models"]), 2)
        self.assertEqual(result["slugs"], ["inversion", "bottlenecks"])
        self.assertIn("shared_keywords", result)
        self.assertIn("unique_keywords", result)
        self.assertIsInstance(result["shared_keywords"], list)
        self.assertIsInstance(result["unique_keywords"], dict)

    def test_compare_three_models(self):
        result = compare_models(["inversion", "bottlenecks", "second-order_thinking"])
        self.assertEqual(len(result["models"]), 3)

    def test_cross_category_span(self):
        # inversion = General Thinking, bottlenecks = Systems Thinking
        result = compare_models(["inversion", "bottlenecks"])
        self.assertGreater(result["categories_spanned"], 1)

    def test_same_category_span_is_one(self):
        # Both in General Thinking
        result = compare_models(["inversion", "first-principle_thinking"])
        self.assertEqual(result["categories_spanned"], 1)

    def test_models_have_structured_sections(self):
        result = compare_models(["inversion", "bottlenecks"])
        for md in result["models"]:
            self.assertIn("thinking_steps", md)
            self.assertIn("when_to_avoid", md)
            self.assertIn("slug", md)

    def test_unknown_slug_raises_key_error(self):
        with self.assertRaises(KeyError):
            compare_models(["inversion", "definitely_not_a_real_slug_xyz"])

    def test_too_few_slugs_raises_value_error(self):
        with self.assertRaises(ValueError):
            compare_models(["inversion"])

    def test_too_many_slugs_raises_value_error(self):
        with self.assertRaises(ValueError):
            compare_models(["inversion", "bottlenecks", "leverage", "debt"])


class TestRandomModel(unittest.TestCase):
    def test_returns_model_instance(self):
        m = random_model()
        self.assertIsInstance(m, Model)
        self.assertTrue(m.slug)
        self.assertTrue(m.name)

    def test_with_category_filter(self):
        cats = list_categories()
        self.assertGreater(len(cats), 0)
        m = random_model(category=cats[0])
        self.assertEqual(m.category.lower(), cats[0].lower())

    def test_unknown_category_raises_value_error(self):
        with self.assertRaises(ValueError):
            random_model(category="no-such-category-xyz")


if __name__ == "__main__":
    unittest.main()
