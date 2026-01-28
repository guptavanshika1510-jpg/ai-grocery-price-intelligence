import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv("../data/prices.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Create a numerical day index (0,1,2,3...)
df["day_number"] = np.arange(len(df))

# Features (X) and target (y)
X = df[["day_number"]]
y = df["price"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict next day's price
next_day = [[df["day_number"].max() + 1]]
predicted_price = model.predict(next_day)[0]

# Determine trend
last_price = df["price"].iloc[-1]

print("Last recorded price:", last_price)
print("Predicted next price:", round(predicted_price, 2))

if predicted_price > last_price:
    print("📈 Price likely to INCREASE → Buy now")
elif predicted_price < last_price:
    print("📉 Price likely to DECREASE → Wait")
else:
    print("➡ Price likely to remain STABLE")
