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


if __name__ == "__main__":
    unittest.main()
