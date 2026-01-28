import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "prices.csv")


URL = "https://webscraper.io/test-sites/e-commerce/static"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers, timeout=10)

print("Status code:", response.status_code)

if response.status_code != 200:
    print("Failed to fetch page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Find first product card
product_card = soup.find("div", class_="thumbnail")

if not product_card:
    print("No product found on page")
    exit()

product_name = product_card.find("a", class_="title").text.strip()
price_text = product_card.find("h4", class_="price").text.strip()
price = float(price_text.replace("$", ""))

today = date.today()

data = {
    "date": [today],
    "product": [product_name],
    "store": ["DemoStore"],
    "price": [price]
}

df = pd.DataFrame(data)

csv_path = csv_path
if os.path.exists(csv_path):
    df.to_csv(csv_path, mode="a", header=False, index=False)
else:
    df.to_csv(csv_path, index=False)

print("✅ Price scraped & saved successfully")
print(df)
