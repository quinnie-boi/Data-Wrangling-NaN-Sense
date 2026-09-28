from constants import CLEANED_AIRBNB_FILE, UNCLEANED_AIRBNB_FILE, UNCLEANED_AIRBNB_DIR
import pandas as pd
import os

def days_since_review(data):
    """how many days since the last review??"""
    return (pd.to_datetime("2026-06-22",format="%Y-%m-%d") - data["last_review"]).dt.days

def cleaned_airbnb_dataset():
    df = pd.read_csv(UNCLEANED_AIRBNB_FILE)

    df["last_review"] = pd.to_datetime(df["last_review"])


    df.drop(axis=1, labels=[
        "name",
        "host_name",
        "neighbourhood_group",
        "minimum_nights",
        "reviews_per_month",
        "license"
    ], inplace=True)


    df["days_since_last_review"] = days_since_review(df)

    for category in ["neighbourhood", "room_type"]:
        df[category] = df[category].astype("category")

    # drop nulls for prices in airbnb
    df.dropna(subset=["price"], inplace=True)

    # Determine latest date available in both datasets
    newest = df["last_review"].max()


    # Airbnb listing data is only valid from October 2025 onwards
    oldest = pd.to_datetime("2025-10-01")

    # Filter Airbnb data
    airbnb_data = df[
        df["last_review"].between(oldest, newest)
    ].copy()

    return df


def main():
    """

    """
    # Write the copy to out folder
    cleaned_airbnb_listings = cleaned_airbnb_dataset()
    # check out_drive
    os.makedirs(
        os.path.dirname(CLEANED_AIRBNB_FILE),
        exist_ok=True)

    cleaned_airbnb_listings.to_csv(
        CLEANED_AIRBNB_FILE,
        index=False)
    print("Airbnb data cleaned successfully.")

if __name__ == "__main__":
    main()