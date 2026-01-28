import pandas as pd

# Load data
df = pd.read_csv("../data/prices.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Calculate statistics
mean_price = df["price"].mean()
std_price = df["price"].std()

# Define threshold for spike
threshold = mean_price + std_price

print("Average price:", round(mean_price, 2))
print("Standard deviation:", round(std_price, 2))
print("Spike threshold:", round(threshold, 2))
print("\nChecking for price spikes...\n")

# Detect spikes
for index, row in df.iterrows():
    if row["price"] > threshold:
        print(
            f"⚠ PRICE SPIKE on {row['date'].date()} | Price = {row['price']}"
        )
    else:
        print(
            f"Normal price on {row['date'].date()} | Price = {row['price']}"
        )
