# Migration Tool — Kovai.co Task

A Python-based web migration tool that scrapes, structures, and exports 
content to JSON with logging, NLP analysis, and REST API endpoints.

## Features
- Scrapes 1000+ records across 50 pages
- Exports clean structured JSON
- Generates migration summary report with NLP keywords
- Logs every action with timestamps
- Handles errors gracefully without crashing
- REST API via FastAPI (with Swagger docs) and Flask

## Project Structure
migration_tool/
├── main.py             → Entry point (run everything locally)
├── api.py              → FastAPI REST endpoints
├── flask_api.py        → Flask REST endpoints
├── scraper.py          → Multi-page scraping logic
├── exporter.py         → JSON export module
├── reporter.py         → Migration report + NLP insights
├── nlp_analyzer.py     → Keyword extraction using spaCy
├── logger.py           → Logging setup
├── requirements.txt    → All dependencies
├── output.json         → Scraped data (1000 records)
├── migration_report.json → Summary with keywords
├── migration.log       → Full activity log
└── README.md           → This file

## How to Run

### Terminal Mode
pip install -r requirements.txt
python main.py

### FastAPI Mode
uvicorn api:app --reload
Visit: http://127.0.0.1:8000/docs

### Flask Mode
python flask_api.py
Visit: http://127.0.0.1:5000

## API Endpoints
| Endpoint   | Method | Description          |
|------------|--------|----------------------|
| /          | GET    | Health check         |
| /migrate   | POST   | Run migration        |
| /data      | GET    | Get all records      |
| /report    | GET    | Get migration report |

## Output
- output.json → all migrated records
- migration_report.json → summary stats + keywords
- migration.log → full activity trail