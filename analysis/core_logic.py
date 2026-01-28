import pandas as pd

# ---------------- DATA PREPARATION ----------------
def prepare_data(csv_path):
    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename storage -> store if needed
    if "storage" in df.columns:
        df = df.rename(columns={"storage": "store"})

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # 🔥 HARD NORMALIZATION (THIS FIXES YOUR ISSUE)
    df["product"] = (
        df["product"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["store"] = (
        df["store"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.replace("\u00a0", "", regex=False)
        .str.lower()
    )

    # Parse dates safely
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    # Drop invalid rows
    df = df.dropna(subset=["date", "product", "store", "price"])

    return df



# ---------------- BUSINESS LOGIC ----------------
def get_product_data(df, product_name):
    product_name = product_name.strip().lower()

    product_df = df[df["product"] == product_name]

    return product_df if not product_df.empty else None


def get_latest_prices(product_df):
    latest_date = product_df["date"].max()
    latest_prices = product_df[product_df["date"] == latest_date]
    return latest_date, latest_prices


def get_cheapest_store(latest_prices):
    if latest_prices.empty:
        return None
    return latest_prices.sort_values(by="price").iloc[0]


def get_best_store_overall(product_df):
    if product_df["store"].nunique() <= 1:
        return None

    avg_prices = (
        product_df
        .groupby("store")["price"]
        .mean()
        .sort_values()
    )

    return avg_prices.index[0], round(avg_prices.iloc[0], 2)
