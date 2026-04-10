"""Tests for mental_models.utils — public utilities for model serialization and parsing."""
import unittest

from mental_models import get_model, load_index
from mental_models.utils import model_to_dict, read_model_markdown, extract_sections


class TestModelToDict(unittest.TestCase):
    def test_all_expected_keys_present(self):
        m = get_model("inversion")
        d = model_to_dict(m)
        for key in ("slug", "name", "category", "keywords", "description", "path", "id"):
            self.assertIn(key, d)

    def test_keywords_is_list(self):
        m = get_model("inversion")
        d = model_to_dict(m)
        self.assertIsInstance(d["keywords"], list)

    def test_round_trip_slug(self):
        m = get_model("bottlenecks")
        d = model_to_dict(m)
        self.assertEqual(d["slug"], m.slug)
        self.assertEqual(d["name"], m.name)


class TestReadModelMarkdown(unittest.TestCase):
    def test_returns_content_for_known_model(self):
        m = get_model("inversion")
        md = read_model_markdown(m)
        self.assertIsInstance(md, str)
        self.assertGreater(len(md), 100)
        self.assertIn("Inversion", md)

    def test_empty_path_returns_empty(self):
        from mental_models.index import Model
        m = Model(slug="fake", name="Fake", category="", keywords=(), description="", path="", id="")
        self.assertEqual(read_model_markdown(m), "")


class TestExtractSections(unittest.TestCase):
    def test_parses_canonical_sections(self):
        m = get_model("inversion")
        md = read_model_markdown(m)
        sections = extract_sections(md)
        self.assertIn("description", sections)
        self.assertIn("thinking steps", sections)
        self.assertIn("when to avoid", sections)
        self.assertGreater(len(sections["thinking steps"]), 50)

    def test_empty_input_returns_empty_dict(self):
        self.assertEqual(extract_sections(""), {})

    def test_no_sections_returns_empty_dict(self):
        self.assertEqual(extract_sections("Just some plain text."), {})


if __name__ == "__main__":
    unittest.main()
