import io
import sys
import unittest

from mental_models import select_models
from mental_models.cli import main as cli_main


class TestSelector(unittest.TestCase):
    def test_select_models_basic_query(self):
        results = select_models("how do I decide between two jobs", top_k=5)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 5)
        # All returned items are Model instances with slugs
        for m in results:
            self.assertTrue(m.slug)
            self.assertTrue(m.name)

    def test_select_models_top_k_respected(self):
        results = select_models("thinking inversion probability risk", top_k=3)
        self.assertLessEqual(len(results), 3)

    def test_select_models_empty_query(self):
        results = select_models("", top_k=5)
        self.assertEqual(results, [])

    def test_cli_runs_and_prints(self):
        buf = io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rc = cli_main(["how", "do", "I", "decide", "between", "two", "jobs"])
        finally:
            sys.stdout = old
        self.assertEqual(rc, 0)
        output = buf.getvalue()
        self.assertIn("Top", output)
        self.assertIn("mental models for", output)


if __name__ == "__main__":
    unittest.main()
