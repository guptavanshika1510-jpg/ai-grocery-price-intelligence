import pandas as pd

df = pd.read_csv("../data/prices.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Standardize column name
df = df.rename(columns={"storage": "store"})

# Handle mixed date formats safely
df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=True)

print("Columns:", df.columns.tolist())
print("Date sample:", df["date"].head())

# Choose product and date
product_name = "Milk"

latest_date = df[df["product"] == product_name]["date"].max()

print("\nComparing prices for:", product_name)
print("Date:", latest_date.date())
print("-" * 40)

filtered = df[
    (df["product"] == product_name) &
    (df["date"] == latest_date)
].sort_values(by="price")

if filtered.empty:
    print("\n⚠ No data available for this product on the selected date.")
    exit()

print(filtered[["store", "price"]])

cheapest = filtered.iloc[0]

print("\n✅ Cheapest Store Today:")
print(f"Store: {cheapest['store']}")
print(f"Price: ₹{cheapest['price']}")
