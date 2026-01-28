import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("../data/prices.csv")

# Convert date column to datetime (VERY IMPORTANT)
df["date"] = pd.to_datetime(df["date"])

print("Dataset:")
print(df)

print("\nAverage Price:", df["price"].mean())
print("Maximum Price:", df["price"].max())
print("Minimum Price:", df["price"].min())

# ---- PLOT PRICE TREND ----
plt.figure(figsize=(8, 4))
plt.plot(df["date"], df["price"], marker="o")

plt.title("Grocery Price Trend")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
