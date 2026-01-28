from fastapi import FastAPI, Query
import os
import pandas as pd

from analysis.core_logic import (
    prepare_data,
    get_product_data,
    get_latest_prices,
    get_cheapest_store,
    get_best_store_overall
)

app = FastAPI(title="Price Intelligence API")

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "prices.csv")


# ---------------- HELPER: LOAD FRESH DATA ----------------
def get_df():
    df = prepare_data(DATA_PATH)

    # Extra safety
    df = df.dropna(subset=["date", "product", "price", "store"])

    return df


# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Price Intelligence API is running"}


# ---------------- PRODUCTS ----------------
@app.get("/products")
def get_products():
    df = get_df()

    products = sorted(df["product"].unique().tolist())

    return {"products": products}


# ---------------- CHEAPEST STORE ----------------
@app.get("/cheapest")
def cheapest_store(product: str = Query(..., description="Product name")):
    df = get_df()
    product = product.strip().lower()

    product_df = get_product_data(df, product)

    if product_df is None:
        return {"error": "Product not found"}

    latest_date, latest_prices = get_latest_prices(product_df)
    cheapest = get_cheapest_store(latest_prices)

    if cheapest is None:
        return {"error": "No price data available"}

    return {
        "product": product,
        "date": str(latest_date.date()),
        "store": cheapest["store"],
        "price": float(cheapest["price"])
    }


# ---------------- BEST STORE ----------------
@app.get("/best-store")
def best_store(product: str = Query(..., description="Product name")):
    df = get_df()
    product = product.strip().lower()

    product_df = get_product_data(df, product)

    if product_df is None:
        return {"error": "Product not found"}

    result = get_best_store_overall(product_df)

    if result is None:
        return {"message": "Only one store available for this product"}

    store, avg_price = result

    return {
        "product": product,
        "best_store": store,
        "average_price": avg_price
    }


# ---------------- PRICE TREND ----------------
@app.get("/trend")
def price_trend(product: str = Query(..., description="Product name")):
    df = get_df()
    product = product.strip().lower()

    product_df = get_product_data(df, product)

    if product_df is None:
        return {"error": "Product not found"}

    trend = []

    for store in product_df["store"].unique():
        store_df = product_df[product_df["store"] == store]

        trend.append({
            "store": store,
            "dates": store_df["date"].astype(str).tolist(),
            "prices": store_df["price"].tolist()
        })

    return {
        "product": product,
        "trend": trend
    }
