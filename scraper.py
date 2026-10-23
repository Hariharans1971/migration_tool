"""Respectful, testable scraper for the Books to Scrape practice website."""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Callable

import requests
from bs4 import BeautifulSoup

from exporter import save_to_json
from logger import setup_logger

BASE_URL = "https://books.toscrape.com/catalogue/page-{page}.html"
USER_AGENT = (
    "Mozilla/5.0 (compatible; PortfolioPracticeScraper/1.0; "
    "+https://github.com/Hariharans1971/migration_tool)"
)
REQUEST_TIMEOUT_SECONDS = 10


def parse_book_page(html: str) -> list[dict[str, str]]:
    """Parse one HTML page into validated book records; no network is used here."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("article.product_pod")
    if not cards:
        raise ValueError("No book cards found; the page structure may have changed.")

    records: list[dict[str, str]] = []
    for index, card in enumerate(cards, start=1):
        title_link = card.select_one("h3 a[title]")
        price_element = card.select_one("p.price_color")
        availability_element = card.select_one("p.instock")

        if title_link is None or price_element is None or availability_element is None:
            raise ValueError(f"Book card {index} is missing a required title, price, or availability field.")

        title = (title_link.get("title") or "").strip()
        price = price_element.get_text(" ", strip=True).replace("\xa0", " ")
        availability = availability_element.get_text(" ", strip=True)
        if not title or not price or not availability:
            raise ValueError(f"Book card {index} contains a blank required field.")

        records.append(
            {
                "title": title,
                "price": price,
                "availability": availability,
            }
        )
    return records


def scrape_all_pages(
    page_count: int = 50,
    output_path: str | Path = "output.json",
    *,
    request_get: Callable[..., requests.Response] | None = None,
    sleep: Callable[[float], None] = time.sleep,
    page_delay: float = 0.25,
    max_retries: int = 3,
    retry_delay: float = 0.5,
    logger: logging.Logger | None = None,
) -> list[dict[str, str]]:
    """Fetch pages with a bounded retry policy and export records to JSON.

    request_get and sleep are injectable so tests can run without live network
    calls or real delays. Only requests-layer errors and known page-parse errors
    are retried; unrelated programmer errors are allowed to surface.
    """
    if page_count < 1:
        raise ValueError("page_count must be at least 1.")
    if max_retries < 1:
        raise ValueError("max_retries must be at least 1.")
    if page_delay < 0 or retry_delay < 0:
        raise ValueError("Delays must be non-negative.")

    fetch = request_get or requests.get
    active_logger = logger or setup_logger()
    headers = {"User-Agent": USER_AGENT}
    books_data: list[dict[str, str]] = []
    failed_pages: list[int] = []

    for page_number in range(1, page_count + 1):
        url = BASE_URL.format(page=page_number)
        page_records: list[dict[str, str]] | None = None

        for attempt in range(1, max_retries + 1):
            try:
                response = fetch(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
                response.raise_for_status()
                page_records = parse_book_page(response.text)
                active_logger.info(
                    "Fetched page %s with %s book records on attempt %s.",
                    page_number,
                    len(page_records),
                    attempt,
                )
                break
            except (requests.RequestException, ValueError) as exc:
                if attempt < max_retries:
                    delay = retry_delay * (2 ** (attempt - 1))
                    active_logger.warning(
                        "Page %s failed on attempt %s/%s; retrying in %.2fs: %s",
                        page_number,
                        attempt,
                        max_retries,
                        delay,
                        exc,
                    )
                    if delay:
                        sleep(delay)
                else:
                    active_logger.error(
                        "Skipping page %s after %s failed attempts: %s",
                        page_number,
                        max_retries,
                        exc,
                    )

        if page_records is not None:
            books_data.extend(page_records)
            if page_number < page_count and page_delay:
                sleep(page_delay)
        else:
            failed_pages.append(page_number)

    if failed_pages:
        # Never publish a partial scrape as a successful export/report.
        raise RuntimeError(
            f"Scrape incomplete: failed to validate or fetch page(s) {failed_pages}. "
            "No JSON export was written; correct the source or retry the run."
        )

    save_to_json(books_data, filename=str(output_path))
    active_logger.info("Scrape finished with %s records across %s requested pages.", len(books_data), page_count)
    return books_data


if __name__ == "__main__":
    records = scrape_all_pages()
    print(f"Finished. Exported {len(records)} book records to output.json.")
