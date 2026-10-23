"""Generate a safe, reproducible summary from exported book records."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nlp_analyzer import extract_keywords

REQUIRED_FIELDS = {"title", "price", "availability"}


def generate_report(
    filename: str | Path = "output.json",
    report_filename: str | Path = "migration_report.json",
) -> dict[str, Any]:
    """Validate exported records and write a report, rejecting invalid/empty input."""
    input_path = Path(filename)
    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError("The export must be a JSON array of book records.")
    if not data:
        raise ValueError("No book records found. Check the scraper output before reporting.")

    prices: list[float] = []
    titles: list[str] = []
    for index, record in enumerate(data, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"Record {index} must be a JSON object.")
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            raise ValueError(f"Record {index} is missing required fields: {sorted(missing)}")

        title = str(record["title"]).strip()
        price_text = str(record["price"]).replace("£", "").replace("\xa0", " ").strip()
        availability = str(record["availability"]).strip()
        if not title or not price_text or not availability:
            raise ValueError(f"Record {index} contains a blank required field.")
        try:
            price = float(price_text)
        except ValueError as exc:
            raise ValueError(f"Record {index} has an invalid price value.") from exc
        if price < 0:
            raise ValueError(f"Record {index} has a negative price.")

        titles.append(title)
        prices.append(price)

    report: dict[str, Any] = {
        "total_books_migrated": len(data),
        "average_price": round(sum(prices) / len(prices), 2),
        "most_expensive": round(max(prices), 2),
        "cheapest": round(min(prices), 2),
        "top_keywords": extract_keywords(" ".join(titles)),
        "status": "Migration Successful",
    }

    output_path = Path(report_filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("=== MIGRATION REPORT ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    return report
