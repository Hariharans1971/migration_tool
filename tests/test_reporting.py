from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import nlp_analyzer
from nlp_analyzer import extract_keywords
from reporter import generate_report


class KeywordExtractionTests(unittest.TestCase):
    def test_fallback_keyword_extraction_is_deterministic(self):
        with patch.object(nlp_analyzer, "nlp", None):
            result = extract_keywords("book prices book titles book availability")
        self.assertEqual(result, ["book", "prices", "titles", "availability"])

    def test_blank_text_returns_no_keywords(self):
        self.assertEqual(extract_keywords("   "), [])

    def test_invalid_limit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "limit"):
            extract_keywords("a sample phrase", limit=0)


class ReportGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.input_path = root / "records.json"
        self.output_path = root / "migration_report.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_report_contains_reproducible_summary(self):
        records = [
            {"title": "A Light in the Attic", "price": "£51.77", "availability": "In stock"},
            {"title": "Tipping the Velvet", "price": "£53.74", "availability": "In stock"},
        ]
        self.input_path.write_text(json.dumps(records), encoding="utf-8")

        with patch.object(nlp_analyzer, "nlp", None):
            report = generate_report(self.input_path, self.output_path)

        self.assertEqual(report["total_books_migrated"], 2)
        self.assertEqual(report["cheapest"], 51.77)
        self.assertEqual(report["most_expensive"], 53.74)
        self.assertEqual(json.loads(self.output_path.read_text(encoding="utf-8")), report)

    def test_report_rejects_empty_exports(self):
        self.input_path.write_text("[]", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "No book records"):
            generate_report(self.input_path, self.output_path)

    def test_report_rejects_non_array_exports(self):
        self.input_path.write_text('{"title": "not a list"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "JSON array"):
            generate_report(self.input_path, self.output_path)

    def test_report_rejects_invalid_price(self):
        self.input_path.write_text(
            json.dumps([{"title": "Example book", "price": "unknown", "availability": "In stock"}]),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "invalid price"):
            generate_report(self.input_path, self.output_path)


if __name__ == "__main__":
    unittest.main()
