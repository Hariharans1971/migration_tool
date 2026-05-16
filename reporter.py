import json
from nlp_analyzer import extract_keywords

def generate_report(filename="output.json"):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    prices = [float(item["price"].replace("£", "")) for item in data]
    
    all_titles = " ".join([item["title"] for item in data])
    keywords = extract_keywords(all_titles)
    
    report = {
        "total_books_migrated": total,
        "average_price": round(sum(prices) / len(prices), 2),
        "most_expensive": max(prices),
        "cheapest": min(prices),
        "top_keywords": keywords,
        "status": "Migration Successful"
    }

    with open("migration_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("=== MIGRATION REPORT ===")
    for key, value in report.items():
        print(f"{key}: {value}")