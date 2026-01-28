import pandas as pd

# Load data
df = pd.read_csv("../data/prices.csv")

# Normalize columns
df.columns = df.columns.str.strip().str.lower()
df = df.rename(columns={"storage": "store"})

# Handle mixed date formats
df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=True)

product_name = "Milk"

product_df = df[df["product"] == product_name]

if product_df.empty:
    print("No data available for product:", product_name)
    exit()

# Latest available date for this product
latest_date = product_df["date"].max()

latest_prices = product_df[product_df["date"] == latest_date]

# Cheapest today
cheapest_today = latest_prices.sort_values(by="price").iloc[0]

# Average price per store
avg_prices = (
    product_df
    .groupby("store")["price"]
    .mean()
    .sort_values()
)

print("📅 Latest Date:", latest_date.date())
print("\n🟢 Cheapest Store Today:")
print(f"Store: {cheapest_today['store']}")
print(f"Price: ₹{cheapest_today['price']}")

print("\n📊 Best Store Overall (Historical Average):")
print(f"Store: {avg_prices.index[0]}")
print(f"Average Price: ₹{round(avg_prices.iloc[0], 2)}")
