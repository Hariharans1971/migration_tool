# Migration Tool — Web Data Extraction and Reporting

[![Scraper tests](https://github.com/Hariharans1971/migration_tool/actions/workflows/tests.yml/badge.svg)](https://github.com/Hariharans1971/migration_tool/actions/workflows/tests.yml)

[![Scraper tests](https://github.com/Hariharans1971/migration_tool/actions/workflows/tests.yml/badge.svg)](https://github.com/Hariharans1971/migration_tool/actions/workflows/tests.yml)

A Python learning project that scrapes the public Books to Scrape demo site, structures book listing data, exports JSON, and creates a summary report. It also contains small Flask and FastAPI endpoint examples.

> Use this project only with sites you are authorized to access. Respect each site's terms, robots rules, rate limits, and applicable law. This demo is not a general-purpose production migration platform.

## Features

- Extracts book titles, prices, and availability from the Books to Scrape practice website.
- Exports structured JSON and produces a summary report.
- Applies request timeouts, bounded exponential retries, HTTP status validation, and a small delay between successful pages.
- Keeps HTML parsing separate from network access so it can be tested with saved fixtures.
- Includes mocked HTTP tests; CI does not depend on the live website.

## Project files

```text
api.py
flask_api.py
main.py
scraper.py
exporter.py
reporter.py
nlp_analyzer.py
logger.py
requirements.txt
README.md
```

Generated output files and runtime logs are intentionally not tracked. Running the application creates fresh output for your local experiment.

## Run locally

```bash
git clone https://github.com/Hariharans1971/migration_tool.git
cd migration_tool
python -m venv .venv
python -m pip install -r requirements.txt
python main.py
```

Activate the environment first on Windows or macOS/Linux. Inspect `main.py` and `scraper.py` to understand which output paths and request settings are used.

API examples, if their dependencies are installed:

```bash
uvicorn api:app --reload
python flask_api.py
```

Check the route definitions in `api.py` and `flask_api.py` for current endpoints.

## Automated checks

Run the offline tests with the lightweight scraper dependencies:

```bash
python -m pip install requests beautifulsoup4
python -m unittest discover -s tests -v
```

The tests use saved HTML and mocked HTTP responses to verify extraction, HTTP-error handling, retries, and JSON export without scraping the live site.

## Engineering limitations

- The scraper targets a practice site and its current HTML structure; page changes can break parsing.
- Do not assume the reported number of records without running and checking the output.
- The scraper validates HTTP status and required page elements, but the overall demo is not a production migration framework.
- Keyword extraction uses the spaCy English model when installed and falls back to deterministic token counting when it is unavailable.
- If any requested page fails validation or exhausts retries, the scraper raises an error and does not write a partial export that could be mislabeled successful.
- Avoid committing generated logs, large output dumps, secrets, or personal data.

## Roadmap

- Add structured run summaries for successful page count, record count, and failure causes.
- Add schema versioning to exported JSON and reporting output.
- Consider a separately labelled partial-export mode only if users need it.

## Author

Hariharan S. — B.Tech Computer Science and Engineering (AI & ML), 2026
