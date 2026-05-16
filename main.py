from scraper import scrape_all_pages
from reporter import generate_report

if __name__ == "__main__":
    print("🚀 Starting Migration...")
    scrape_all_pages()
    generate_report()
    print("✅ Migration Complete!")