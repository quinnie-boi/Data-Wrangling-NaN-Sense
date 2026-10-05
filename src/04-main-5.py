"""
Combine Airbnb and Rental Bond datasets and produce
the required summary statistics.
"""

import pandas as pd

from constants import (
    CLEANED_AIRBNB_SA2_FILE,
    CLEANED_BONDS_FILE,
    CLEANED_MERGED_DATASET_FILE
)


def med_airbnb_price(location_id, filename):
    """
    Return the median Airbnb price for a given SA2 location.

    Missing and non-numeric prices are excluded.
    """

    df = pd.read_csv(filename)

    # Ensure SA2 codes are numeric
    df["sa2_code"] = pd.to_numeric(
        df["sa2_code"],
        errors="coerce"
    )

    # Ensure prices are numeric
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Filter to specified SA2 location
    df = df[
        df["sa2_code"] == location_id
    ].copy()

    return df["price"].median()


def compare_dataset_location_population(
    filename=CLEANED_MERGED_DATASET_FILE
):
    """
    Print areas with the largest number of Airbnb listings
    alongside Rental Bond counts.
    """

    df = pd.read_csv(filename)

    summary = (
        df.groupby("sa2_name")
        .agg(
            airbnb_listings=("id", "count"),
            active_bonds=("Active Bonds", "first"),
            total_bonds=("Total Bonds", "first")
        )
        .sort_values(
            "airbnb_listings",
            ascending=False
        )
        .head()
    )
    summary["active_bonds"] = summary["active_bonds"].astype("Int64")
    summary["total_bonds"] = summary["total_bonds"].astype("Int64")
    print(summary)


def merge_rental_bonds_and_chch_listings():
    """
    Merge cleaned Airbnb and Rental Bond datasets
    using SA2 code and quarter.

    Airbnb can contain many listings for each SA2-quarter.
    Rental Bond data should contain no more than one
    observation for each SA2-quarter.
    """

    # ------------------------------------------------------------------
    # Read datasets
    # ------------------------------------------------------------------

    airbnb = pd.read_csv(
        CLEANED_AIRBNB_SA2_FILE
    )

    bond = pd.read_csv(
        CLEANED_BONDS_FILE
    )

    # ------------------------------------------------------------------
    # Standardise SA2 codes
    # ------------------------------------------------------------------

    airbnb["sa2_code"] = pd.to_numeric(
        airbnb["sa2_code"],
        errors="coerce"
    ).astype("Int64")

    bond["sa2_code"] = pd.to_numeric(
        bond["sa2_code"],
        errors="coerce"
    ).astype("Int64")

    # ------------------------------------------------------------------
    # Create matching quarter columns
    # ------------------------------------------------------------------

    # Construct Airbnb scrape date from scrape year/month
    airbnb["listing_date"] = pd.to_datetime(
        airbnb.assign(
            year=airbnb["scrape_year"] + 2000,
            month=airbnb["scrape_month"],
            day=1
        )[
            ["year", "month", "day"]
        ]
    )

    # Convert Airbnb scrape date to quarterly period
    airbnb["quarter"] = (
        airbnb["listing_date"]
        .dt.to_period("Q")
    )
    # Keep one aggregate Rental Bond observation per area/time period
    bond = bond[
        (bond["Dwelling Type"] == "ALL")
        & (bond["Number Of Beds"] == "ALL")
        ].copy()
    # Convert Rental Bond TimeFrame to quarterly period
    bond["quarter"] = (
        pd.to_datetime(
            bond["TimeFrame"]
        )
        .dt.to_period("Q")
    )

    # ------------------------------------------------------------------
    # Check merge keys
    # ------------------------------------------------------------------

    duplicate_pairs = bond.duplicated(
        ["sa2_code", "quarter"]
    ).sum()

    print(
        "Bond duplicate SA2-quarter pairs:",
        duplicate_pairs
    )

    if duplicate_pairs > 0:
        raise ValueError(
            f"Found {duplicate_pairs} duplicate "
            f"SA2-quarter combinations in Rental Bond data."
        )

    # ------------------------------------------------------------------
    # Merge datasets
    # ------------------------------------------------------------------

    joined = airbnb.merge(
        bond,
        on=["sa2_code", "quarter"],
        how="left",
        validate="many_to_one",
        indicator=True
    )

    # ------------------------------------------------------------------
    # Check merge results
    # ------------------------------------------------------------------

    print(
        "Airbnb rows before join:",
        len(airbnb)
    )

    print(
        "Rows after join:",
        len(joined)
    )

    print(
        "Rows matched with Bond:",
        (joined["_merge"] == "both").sum()
    )

    print(
        "Rows without Bond match:",
        (joined["_merge"] == "left_only").sum()
    )

    print("\nMerge results by quarter:")

    print(
        joined.groupby(
            ["quarter", "_merge"],
            observed=True
        )
        .size()
        .unstack(fill_value=0)
    )

    # ------------------------------------------------------------------
    # Show unmatched Airbnb rows by quarter
    # ------------------------------------------------------------------

    print("\nUnmatched Airbnb rows by quarter:")

    print(
        joined.loc[
            joined["_merge"] == "left_only",
            "quarter"
        ]
        .value_counts()
        .sort_index()
    )

    # ------------------------------------------------------------------
    # Remove temporary merge column
    # ------------------------------------------------------------------

    joined.drop(
        columns=["_merge"],
        inplace=True
    )

    # ------------------------------------------------------------------
    # Save merged dataset
    # ------------------------------------------------------------------

    joined.to_csv(
        CLEANED_MERGED_DATASET_FILE,
        index=False
    )

    print(
        "\nJoined dataset saved:",
        CLEANED_MERGED_DATASET_FILE
    )

    print(
        "Final rows:",
        len(joined)
    )

    return joined


def prasanthi(df):
    """
    Determine which Christchurch SA2 areas have the largest
    mean gap between Airbnb prices and long-term rental prices.
    """

    # ------------------------------------------------------------------
    # Ensure price fields are numeric
    # ------------------------------------------------------------------

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["Geometric Mean Rent"] = pd.to_numeric(
        df["Geometric Mean Rent"],
        errors="coerce"
    )

    # ------------------------------------------------------------------
    # Convert weekly Rental Bond rent to nightly equivalent
    # ------------------------------------------------------------------

    df["nightly_rental_rate"] = (
        df["Geometric Mean Rent"] / 7
    ).round(2)

    # ------------------------------------------------------------------
    # Calculate Airbnb versus long-term rental price difference
    # ------------------------------------------------------------------

    df["price_difference"] = (
        df["price"]
        - df["nightly_rental_rate"]
    ).round(2)

    # ------------------------------------------------------------------
    # Calculate mean difference by SA2
    # ------------------------------------------------------------------

    mean_differences = (
        df.groupby(
            ["sa2_code", "sa2_name"]
        )["price_difference"]
        .mean()
        .round(2)
        .reset_index()
    )

    mean_differences.rename(
        columns={
            "price_difference":
                "mean_price_difference"
        },
        inplace=True
    )

    # ------------------------------------------------------------------
    # Sort from largest to smallest difference
    # ------------------------------------------------------------------

    mean_differences_sorted = (
        mean_differences.sort_values(
            by="mean_price_difference",
            ascending=False
        )
    )

    print(
        "\n--- SA2 Areas Ranked by "
        "Mean Price Difference ---"
    )

    print(
        mean_differences_sorted
        .head()
        .to_string(index=False)
    )

    return mean_differences_sorted


def main():
    """
    Merge the Airbnb and Rental Bond datasets,
    then run the required summary analysis.
    """

    # ------------------------------------------------------------------
    # Merge Airbnb and Rental Bond data
    # ------------------------------------------------------------------

    joined = merge_rental_bonds_and_chch_listings()

    # ------------------------------------------------------------------
    # Airbnb versus Rental Bond price analysis
    # ------------------------------------------------------------------

    prasanthi(joined)

    # ------------------------------------------------------------------
    # Median Airbnb price for Christchurch Central
    # ------------------------------------------------------------------

    # Calculate Airbnb median directly from the Airbnb + SA2 file.
    # Rental Bond data is not needed for this statistic.
    median_price = med_airbnb_price(
        326600,
        CLEANED_AIRBNB_SA2_FILE
    )

    print(
        "\n"
        + "#" * 10
        + " Median Price "
        + "#" * 10
    )

    print(
        f"Median Airbnb price for Christchurch Central "
        f"(SA2: 326600): ${median_price:.2f}"
    )

    # ------------------------------------------------------------------
    # Compare Airbnb listings and Rental Bond population
    # ------------------------------------------------------------------

    print(
        "\n"
        + "#" * 10
        + " Compare Airbnb listings and Rental Bonds "
        + "#" * 10
    )

    compare_dataset_location_population(
        CLEANED_MERGED_DATASET_FILE
    )

    print("\nNo errors")


if __name__ == "__main__":
    main()