import pandas as pd
import random
from datetime import datetime, timedelta
import os

# ---------------- CONFIG ----------------
PRODUCTS = {
    "Milk": {"base_price": 55, "stores": ["StoreA", "StoreB", "StoreC"]},
    "Rice": {"base_price": 60, "stores": ["StoreA", "StoreB"]},
    "Bread": {"base_price": 40, "stores": ["StoreA", "StoreC"]},
    "Eggs": {"base_price": 6, "stores": ["StoreB", "StoreC"]},
}

DAYS = 90  # number of historical days
OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "prices.csv"
)

# ---------------- LOGIC ----------------
def generate_data():
    rows = []
    today = datetime.today()

    for product, info in PRODUCTS.items():
        for store in info["stores"]:
            price = info["base_price"]

            for i in range(DAYS):
                date = today - timedelta(days=DAYS - i)

                # daily fluctuation
                price_change = random.uniform(-0.05, 0.05)
                price += price * price_change

                # occasional spike
                if random.random() < 0.05:
                    price += random.uniform(3, 8)

                price = round(price, 2)

                rows.append({
                    "date": date.strftime("%d-%m-%Y"),
                    "product": product,
                    "store": store,
                    "price": price
                })

    return pd.DataFrame(rows)

# ---------------- RUN ----------------
if __name__ == "__main__":
    new_df = generate_data()

    if os.path.exists(OUTPUT_PATH):
        old_df = pd.read_csv(OUTPUT_PATH)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df.to_csv(OUTPUT_PATH, index=False)
    print("✅ Historical data generated and appended successfully")
