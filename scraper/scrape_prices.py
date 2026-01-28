import pandas as pd
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "prices.csv")

# ---------------- PRODUCT CONFIG ----------------
# NOTE: These URLs are placeholders.
# We will replace them with real public pages later.
PRODUCTS = [
    {
        "product": "rice",
        "store": "storea",
        "url": "https://example.com/rice-a"
    },
    {
        "product": "rice",
        "store": "storeb",
        "url": "https://example.com/rice-b"
    },
    {
        "product": "milk",
        "store": "storea",
        "url": "https://example.com/milk-a"
    },
    {
        "product": "milk",
        "store": "storeb",
        "url": "https://example.com/milk-b"
    },
]

# ---------------- REAL SCRAPER ----------------
def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Example selector (site-dependent)
    price_tag = soup.select_one("span.price")

    if not price_tag:
        raise ValueError("Price not found on page")

    price_text = price_tag.text.strip()
    price_text = price_text.replace("₹", "").replace(",", "")

    return float(price_text)

# ---------------- MAIN SCRAPER ----------------
def run_scraper():
    today = datetime.now().strftime("%d-%m-%Y")
    rows = []

    for item in PRODUCTS:
        try:
            price = scrape_price(item["url"])
            print(f"Scraped {item['product']} from {item['store']}: {price}")
        except Exception as e:
            print(f"Failed for {item['product']} ({item['store']}): {e}")
            continue

        rows.append({
            "date": today,
            "product": item["product"],
            "price": price,
            "store": item["store"]
        })

    if not rows:
        print("No data scraped. CSV not updated.")
        return

    df_new = pd.DataFrame(rows)

    # Append safely
    if os.path.exists(DATA_PATH):
        df_new.to_csv(DATA_PATH, mode="a", header=False, index=False)
    else:
        df_new.to_csv(DATA_PATH, index=False)

    print("Scraping completed successfully")

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    run_scraper()
