import requests
from bs4 import BeautifulSoup
from exporter import save_to_json
from logger import setup_logger
from reporter import generate_report
def scrape_all_pages():
    # your existing code here
    logger = setup_logger()
    books_data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"
    }
    for i in range(1, 51):
        try:
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            logger.info(f"Fetched page {i} | Status: {response.status_code}")
            
            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article")
            
            for book in books:
                title = book.find("h3").find("a")["title"]
                price = book.find("p", class_="price_color").text.strip()
                availability = book.find("p", class_="instock").text.strip()
                
                books_data.append({
                    "title": title,
                    "price": price,
                    "availability": availability
                })
                logger.info(f"Scraped: {title}")

        except Exception as e:
            logger.error(f"Failed on page {i}: {e}")
            print(f"⚠️ Skipping page {i} — {e}")
            
    save_to_json(books_data)
    logger.info(f"Migration complete. Total books: {len(books_data)}")
    print(f"Done! Total books scraped: {len(books_data)}")