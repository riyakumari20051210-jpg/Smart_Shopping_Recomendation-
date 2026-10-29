import pandas as pd
import os # It is useful for find the correct path of file.
from sklearn.preprocessing import MinMaxScaler  # Its prpcessing technique convert numerical value in common range(0,1) 


def load_data():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "products.csv"
    )

    return pd.read_csv("product.csv")


def recommend_products(category, budget, min_rating=0):

    df = load_data()

    filtered = df[
        (df["category"] == category) &
        (df["price"] <= budget) &
        (df["rating"] >= min_rating)
    ].copy()

    if filtered.empty:
        return filtered

    scaler = MinMaxScaler()

    filtered["rating_score"] = scaler.fit_transform(
        filtered[["rating"]]
    )

    filtered["discount_score"] = scaler.fit_transform(
        filtered[["discount"]]
    )

    filtered["price_score"] = 1 - scaler.fit_transform(
        filtered[["price"]]
    )

    filtered["recommendation_score"] = (
        filtered["rating_score"] * 0.50 +
        filtered["price_score"] * 0.30 +
        filtered["discount_score"] * 0.20
    )

    filtered["recommendation_score"] = (
        filtered["recommendation_score"] * 100
    ).round(2)

    filtered = filtered.sort_values(
        by="recommendation_score",
        ascending=False
    )

    return filtered.head(5)