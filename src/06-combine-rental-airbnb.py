"""
Combine rental and bonds data sets
"""
from constants import CLEANED_AIRBNB_SA2_FILE, CLEANED_MERGED_DATASET_FILE, CLEANED_BONDS_FILE
import pandas as pd


def merge_rental_bonds_and_chch_listings():
    """
    merges our rental bonds dataset with our listings dataset along the sa2 column
    """
    # Written by Syamily :)
    # Tweaked by Quinn

    # Read the datasets
    airbnb = pd.read_csv(CLEANED_AIRBNB_SA2_FILE)

    bond = pd.read_csv(CLEANED_BONDS_FILE)

    # Check the files before joining
    # print("Airbnb rows:", len(airbnb))
    # print("Bond rows:", len(bond))
    # print("Airbnb columns:\n ", ",\n  ".join(airbnb.columns.tolist()))
    # print("Bond columns:\n ", ",\n  ".join(bond.columns.tolist()))

    # Check the result
    # print(
    #     "chch listing dates:\n",
    #     airbnb["listing_date"]
    #     .drop_duplicates()
    #     .head()
    #     .to_string(index=False)
    # )

    # Make sure both datasets use the same area-code format
    if bond['sa2_code'].dtype !=  airbnb['sa2_code'].dtype:
        print(f"rental bonds has sa2_code dtype of {bond['sa2_code'].dtype}")
        print(f"      airbnb has sa2_code dtype of {airbnb['sa2_code'].dtype}")
        raise TypeError("err")


    # # Check that each area has only one Bond row per quarter
    print(
        "Bond duplicate SA2-quarter pairs:",
        bond.duplicated(
            ["sa2_code", "year_quarter"]
        ).sum())


    joined = airbnb.merge(
        bond,
        on=["sa2_code", "year_quarter"],
        how="left",
        validate="many_to_one",
        indicator=True
    )

    # Remove the temporary column used to check matches
    joined = joined.drop(columns=["_merge"])

    # Save the joined dataset as a new CSV
    joined.to_csv(CLEANED_MERGED_DATASET_FILE, index=False)

    print("Joined dataset saved:", CLEANED_MERGED_DATASET_FILE)
    print("Final rows:", len(joined))



merge_rental_bonds_and_chch_listings()