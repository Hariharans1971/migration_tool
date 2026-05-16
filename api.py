from fastapi import FastAPI
from scraper import scrape_all_pages
from reporter import generate_report   
import json

app = FastAPI(title="Migration Tool API", version="1.0")

@app.get("/")
def home():
    return {"message": "Migration Tool API is running", "status": "ok"}

@app.post("/migrate")
def migrate():
    scrape_all_pages()
    generate_report()
    return {"message": "Migration complete", "status": "success"}

@app.get("/data")
def get_data():
    with open("output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"total": len(data), "books": data}
    
@app.get("/report")
def get_report():
    with open("migration_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
    return report
