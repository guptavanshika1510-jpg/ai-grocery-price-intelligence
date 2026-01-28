import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../data/prices.csv")

# Normalize columns
df.columns = df.columns.str.strip().str.lower()
df = df.rename(columns={"storage": "store"})

# Handle mixed date formats
df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=True)

# Select product
product_name = "Milk"

product_df = df[df["product"] == product_name]

if product_df.empty:
    print("No data available for product:", product_name)
    exit()

# Plot price trends for each store
plt.figure(figsize=(8, 5))

for store in product_df["store"].unique():
    store_data = product_df[product_df["store"] == store]
    plt.plot(store_data["date"], store_data["price"], marker="o", label=store)

plt.title(f"Price Trend for {product_name} (Store-wise)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
