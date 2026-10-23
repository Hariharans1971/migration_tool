from __future__ import annotations

import json
import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import requests

from scraper import parse_book_page, scrape_all_pages

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "books_page.html"


class BookPageParserTests(unittest.TestCase):
    def test_parses_required_fields_from_saved_html(self):
        records = parse_book_page(FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["title"], "A Light in the Attic")
        self.assertEqual(records[0]["price"], "£51.77")
        self.assertEqual(records[0]["availability"], "In stock")
        self.assertEqual(set(records[1]), {"title", "price", "availability"})

    def test_rejects_a_non_book_page(self):
        with self.assertRaisesRegex(ValueError, "No book cards"):
            parse_book_page("<html><body>Access denied</body></html>")

    def test_rejects_incomplete_book_cards(self):
        html = '<article class="product_pod"><h3><a title="Missing price">book</a></h3></article>'
        with self.assertRaisesRegex(ValueError, "missing a required"):
            parse_book_page(html)


class ScraperWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = Path(self.temp_dir.name) / "records.json"
        self.logger = logging.getLogger(f"scraper-test-{id(self)}")
        self.logger.addHandler(logging.NullHandler())
        self.sleep_calls: list[float] = []

    def tearDown(self):
        self.temp_dir.cleanup()

    def no_sleep(self, seconds: float):
        self.sleep_calls.append(seconds)

    @staticmethod
    def successful_response():
        response = Mock()
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = FIXTURE.read_text(encoding="utf-8")
        response.raise_for_status.return_value = None
        return response

    def test_retries_timeout_then_exports_records(self):
        request_get = Mock(side_effect=[requests.Timeout("temporary timeout"), self.successful_response()])
        records = scrape_all_pages(
            page_count=1,
            output_path=self.output_path,
            request_get=request_get,
            sleep=self.no_sleep,
            page_delay=0,
            retry_delay=0.25,
            max_retries=2,
            logger=self.logger,
        )

        self.assertEqual(len(records), 2)
        self.assertEqual(request_get.call_count, 2)
        self.assertEqual(request_get.call_args.kwargs["timeout"], 10)
        self.assertEqual(json.loads(self.output_path.read_text(encoding="utf-8")), records)
        self.assertEqual(self.sleep_calls, [0.25])

    def test_http_errors_are_retried_and_page_is_skipped_after_limit(self):
        failed_response = Mock()
        failed_response.status_code = 503
        failed_response.text = "service unavailable"
        failed_response.raise_for_status.side_effect = requests.HTTPError("503 Server Error")
        request_get = Mock(return_value=failed_response)

        records = scrape_all_pages(
            page_count=1,
            output_path=self.output_path,
            request_get=request_get,
            sleep=self.no_sleep,
            page_delay=0,
            retry_delay=0,
            max_retries=2,
            logger=self.logger,
        )

        self.assertEqual(records, [])
        self.assertEqual(request_get.call_count, 2)
        self.assertEqual(json.loads(self.output_path.read_text(encoding="utf-8")), [])

    def test_invalid_retry_configuration_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "page_count"):
            scrape_all_pages(page_count=0, output_path=self.output_path, logger=self.logger)
        with self.assertRaisesRegex(ValueError, "max_retries"):
            scrape_all_pages(page_count=1, max_retries=0, output_path=self.output_path, logger=self.logger)


if __name__ == "__main__":
    unittest.main()
