import unittest

from mental_models import Model, get_model, list_categories, load_index


class TestIndex(unittest.TestCase):
    def test_load_index_returns_models(self):
        models = load_index()
        self.assertIsInstance(models, list)
        self.assertGreater(len(models), 50)
        self.assertIsInstance(models[0], Model)
        self.assertTrue(models[0].slug)
        self.assertTrue(models[0].name)

    def test_get_model_hit_and_miss(self):
        any_model = load_index()[0]
        fetched = get_model(any_model.slug)
        self.assertEqual(fetched.slug, any_model.slug)
        # Case-insensitive
        fetched_upper = get_model(any_model.slug.upper())
        self.assertEqual(fetched_upper.slug, any_model.slug)
        with self.assertRaises(KeyError):
            get_model("definitely-not-a-real-slug-xyz")

    def test_list_categories_nonempty(self):
        cats = list_categories()
        self.assertIsInstance(cats, list)
        self.assertGreater(len(cats), 0)
        self.assertEqual(cats, sorted(cats))
        # Ensure uniqueness
        self.assertEqual(len(cats), len(set(cats)))

    def test_model_has_compiled_sections(self):
        models = load_index()
        # Inversion is a core model that should have all sections populated
        m = next(m for m in models if m.slug == "inversion")
        self.assertTrue(hasattr(m, "thinking_steps"))
        self.assertTrue(hasattr(m, "coaching_questions"))
        self.assertTrue(hasattr(m, "when_to_avoid"))
        self.assertTrue(len(m.thinking_steps) > 50)
        self.assertTrue(len(m.coaching_questions) > 50)
        self.assertTrue(len(m.when_to_avoid) > 50)


if __name__ == "__main__":
    unittest.main()
