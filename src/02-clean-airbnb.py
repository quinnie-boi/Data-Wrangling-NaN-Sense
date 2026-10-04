from constants import CLEANED_AIRBNB_FILE, UNCLEANED_AIRBNB_FILE, UNCLEANED_AIRBNB_DIR
import pandas as pd
import os

def days_since_review(data):
    """how many days since the last review??"""
    return (pd.to_datetime("2026-06-22",format="%Y-%m-%d") - data["last_review"]).dt.days

def cleaned_airbnb_dataset():
    """Clean the combined Christchurch Airbnb dataset."""

    df = pd.read_csv(
        UNCLEANED_AIRBNB_FILE
    )

    # Convert last_review to datetime
    df["last_review"] = pd.to_datetime(
        df["last_review"],
        errors="coerce"
    )

    # Keep Christchurch City listings only
    df = df[
        df["neighbourhood_group"] == "Christchurch City"
    ].copy()

    # Drop unnecessary columns
    df.drop(
        columns=[
            "name",
            "host_name",
            "neighbourhood_group",
            "minimum_nights",
            "reviews_per_month",
            "license"
        ],
        inplace=True
    )

    # Add days since last review
    df["days_since_last_review"] = days_since_review(df)

    # Convert categorical columns
    for category in [
        "neighbourhood",
        "room_type"
    ]:
        df[category] = df[category].astype("category")

    # Remove listings without a usable price
    df.dropna(
        subset=["price"],
        inplace=True
    )

    return df




def main():
    cleaned_airbnb_listings = cleaned_airbnb_dataset()

    os.makedirs(
        os.path.dirname(CLEANED_AIRBNB_FILE),
        exist_ok=True
    )

    cleaned_airbnb_listings.to_csv(
        CLEANED_AIRBNB_FILE,
        index=False
    )

    print("Airbnb data cleaned successfully.")


if __name__ == "__main__":
    main()