import pandas as pd

from constants import (
    CLEANED_AIRBNB_FILE,
    CLEANED_AIRBNB_SA2_FILE,
    JODI_SA2
)


def compare_datasets():
    new_df = pd.read_csv(CLEANED_AIRBNB_SA2_FILE)
    jodi_df = pd.read_csv(JODI_SA2)
    cleaned_df = pd.read_csv(CLEANED_AIRBNB_FILE)

    # Filter both to Christchurch Central
    new_central = new_df[
        new_df["sa2_code"] == 326600
    ].copy()

    jodi_central = jodi_df[
        jodi_df["sa2_code"] == 326600
    ].copy()

    print("========== JODI ==========")
    print("Rows:", len(jodi_central))
    print("Unique IDs:", jodi_central["id"].nunique())
    print("Median:", jodi_central["price"].median())

    print("\n========== NEW ==========")
    print("Rows:", len(new_central))
    print("Unique IDs:", new_central["id"].nunique())
    print("Median:", new_central["price"].median())

    # Get unique IDs from both datasets
    new_ids = set(new_central["id"])
    jodi_ids = set(jodi_central["id"])

    extra_ids = new_ids - jodi_ids

    print("\n========== ID DIFFERENCES ==========")
    print("IDs only in Jodi:", len(jodi_ids - new_ids))
    print("IDs only in new:", len(extra_ids))
    print("IDs in both:", len(new_ids & jodi_ids))

    # Show extra Christchurch Central listings
    extra_listings = new_central[
        new_central["id"].isin(extra_ids)]

    print("\n========== EXTRA LISTINGS BY HOST ==========")

    print(
        extra_listings.groupby("host_id")
        .agg(
            unique_listings=("id", "nunique"),
            observations=("id", "size"),
            median_price=("price", "median")
        )
        .sort_values("unique_listings", ascending=False)
    )

    print("\n========== EXTRA HOSTS IN JODI DATA ==========")

    extra_hosts = set(extra_listings["host_id"])

    for host_id in extra_hosts:
        new_host = new_df[new_df["host_id"] == host_id]
        jodi_host = jodi_df[jodi_df["host_id"] == host_id]

        print(f"\nHost: {host_id}")
        print("New unique listings:", new_host["id"].nunique())
        print("Jodi unique listings:", jodi_host["id"].nunique())

    print("\n========== FULL DATASET COMPARISON ==========")

    print("Jodi total rows:", len(jodi_df))
    print("New total rows:", len(new_df))

    print("Jodi unique listings:", jodi_df["id"].nunique())
    print("New unique listings:", new_df["id"].nunique())

    jodi_all_ids = set(jodi_df["id"])
    new_all_ids = set(new_df["id"])

    print(
        "IDs only in new full dataset:",
        len(new_all_ids - jodi_all_ids)
    )

    print(
        "IDs only in Jodi full dataset:",
        len(jodi_all_ids - new_all_ids)
    )

    print(
        "IDs in both datasets:",
        len(new_all_ids & jodi_all_ids)
    )

    print("\n========== NEW BY SCRAPE ==========")

    print(
        new_df.groupby(
            ["scrape_year", "scrape_month"]
        ).agg(
            rows=("id", "size"),
            unique_listings=("id", "nunique")
        )
    )

    print("\n========== JODI BY SCRAPE ==========")

    print(
        jodi_df.groupby(
            ["scrape_year", "scrape_month"]
        ).agg(
            rows=("id", "size"),
            unique_listings=("id", "nunique")
        )
    )
if __name__ == "__main__":
    compare_datasets()