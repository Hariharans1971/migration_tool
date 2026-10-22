# Migration Tool — Web Data Extraction and Reporting

A Python learning project that scrapes the public Books to Scrape demo site, structures book listing data, exports JSON, and creates a summary report. It also contains small Flask and FastAPI endpoint examples.

> Use this project only with sites you are authorized to access. Respect each site's terms, robots rules, rate limits, and applicable law. This demo is not a general-purpose production migration platform.

## Features

- Extracts book titles, prices, and availability from the Books to Scrape practice website.
- Exports structured JSON.
- Produces a simple summary report and application logs.
- Demonstrates Python modules, error handling, and basic HTTP API patterns.

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

## Engineering limitations

- The scraper targets a practice site and its current HTML structure; page changes can break parsing.
- Do not assume the reported number of records without running and checking the output.
- Add request timeouts, bounded retries, respectful delays, input validation, and automated tests before extending this project.
- Avoid committing generated logs, large output dumps, secrets, or personal data.

## Roadmap

- Add tests with saved HTML fixtures and no live network dependency.
- Add configurable timeout, retry, and rate-limit settings.
- Normalize schema and validate exported records.
- Add reproducible sample outputs and structured error reporting.

## Author

Hariharan S. — B.Tech Computer Science and Engineering (AI & ML), 2026
