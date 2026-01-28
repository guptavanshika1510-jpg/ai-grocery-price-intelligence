from core_logic import *
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "prices.csv")

df = prepare_data(DATA_PATH)

product = "Milk"
product_df = get_product_data(df, product)

latest_date, latest_prices = get_latest_prices(product_df)
cheapest = get_cheapest_store(latest_prices)

print("Product:", product)
print("Latest Date:", latest_date)
print("Cheapest Store:", cheapest["store"], cheapest["price"])
