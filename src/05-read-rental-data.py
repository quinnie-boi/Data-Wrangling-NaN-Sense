from constants import RAW_BONDS_FILE, CLEANED_BONDS_FILE

import pandas as pd


def open_quarterly_dataset(path=RAW_BONDS_FILE):
    """Read the Rental Bond dataset."""

    return pd.read_csv(
        path,
        parse_dates=["TimeFrame"]
    )


def clean_quarterly_dataset():
    """
    Clean and structure the Rental Bond dataset.
    """

    df = open_quarterly_dataset()

    # Remove rows without Median Rent
    df.dropna(
        subset=["Median Rent"],
        inplace=True
    )

    # Remove invalid Location IDs
    df = df[
        df["Location Id"] != -99
    ].copy()

    # Rename Location Id to match Airbnb SA2 code
    df.rename(
        columns={"Location Id": "sa2_code"},
        inplace=True
    )
    df["sa2_code"] = df["sa2_code"].astype("Int64")
    # Keep aggregate dwelling/beds data
    df = df[
        (df["Dwelling Type"] == "ALL") &
        (df["Number Of Beds"] == "ALL")
    ].copy()

    return df


def clean_bonds_dataset():
    """
    Clean the Rental Bond dataset and restrict it
    to the analysis date range.
    """

    rental_bonds_data = clean_quarterly_dataset()

    oldest = pd.to_datetime("2025-10-01")
    newest = pd.to_datetime("2026-06-30")

    # Filter Rental Bond data
    rental_bonds_data = rental_bonds_data[
        rental_bonds_data["TimeFrame"].between(
            oldest,
            newest
        )
    ].copy()

    print(
        f"Data retained from "
        f"{oldest.date()} to {newest.date()}"
    )

    # Save cleaned dataset
    rental_bonds_data.to_csv(
        CLEANED_BONDS_FILE,
        index=False
    )

    print(
        f"Successfully saved the cleaned Rental Bond dataset to "
        f"{CLEANED_BONDS_FILE}"
    )

    return rental_bonds_data


def main():
    clean_bonds_dataset()
    print("No errors")


if __name__ == "__main__":
    main()