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

    def _capture(self, argv):
        import io as _io
        buf = _io.StringIO()
        old = sys.stdout
        sys.stdout = buf
        try:
            rc = cli_main(argv)
        finally:
            sys.stdout = old
        return rc, buf.getvalue()

    def test_cli_select_text(self):
        rc, out = self._capture(["select", "how", "do", "I", "decide", "between", "two", "jobs"])
        self.assertEqual(rc, 0)
        self.assertIn("mental models for", out)

    def test_cli_select_json(self):
        import json as _json
        rc, out = self._capture(["select", "--json", "inversion", "-k", "3"])
        self.assertEqual(rc, 0)
        data = _json.loads(out)
        self.assertIn("models", data)
        self.assertLessEqual(len(data["models"]), 3)

    def test_cli_get_field(self):
        rc, out = self._capture(["get", "inversion", "--field", "name"])
        self.assertEqual(rc, 0)
        self.assertIn("Inversion", out)

    def test_cli_categories_json(self):
        import json as _json
        rc, out = self._capture(["categories", "--json"])
        self.assertEqual(rc, 0)
        cats = _json.loads(out)
        self.assertIsInstance(cats, list)
        self.assertGreater(len(cats), 0)

    def test_cli_apply_json_has_sections(self):
        import json as _json
        rc, out = self._capture(["apply", "inversion", "--problem", "pricing", "strategy", "--json"])
        self.assertEqual(rc, 0)
        data = _json.loads(out)
        self.assertGreater(len(data["thinking_steps"]), 100)
        self.assertGreater(len(data["when_to_avoid"]), 50)

    def test_cli_doctor_ok(self):
        import json as _json
        rc, out = self._capture(["doctor", "--json"])
        self.assertEqual(rc, 0)
        d = _json.loads(out)
        self.assertTrue(d["ok"])
        self.assertGreaterEqual(d["checks"]["model_count"], 90)

    def test_cli_get_not_found(self):
        rc, _ = self._capture(["get", "not_a_real_slug"])
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
