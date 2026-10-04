"""
Diagnostics for the Airbnb and Rental Bond merge.
"""

import pandas as pd

from constants import (
    RAW_BONDS_FILE,
    CLEANED_AIRBNB_SA2_FILE,
    CLEANED_BONDS_FILE,
    CLEANED_MERGED_DATASET_FILE
)


def check_merge():
    airbnb = pd.read_csv(CLEANED_AIRBNB_SA2_FILE)
    bonds = pd.read_csv(CLEANED_BONDS_FILE)
    merged = pd.read_csv(CLEANED_MERGED_DATASET_FILE)
    raw_bonds = pd.read_csv(RAW_BONDS_FILE)

    # Standardise SA2 datatypes for comparisons
    airbnb["sa2_code"] = pd.to_numeric(
        airbnb["sa2_code"],
        errors="coerce"
    ).astype("Int64")

    bonds["sa2_code"] = pd.to_numeric(
        bonds["sa2_code"],
        errors="coerce"
    ).astype("Int64")

    raw_bonds["Location Id"] = pd.to_numeric(
        raw_bonds["Location Id"],
        errors="coerce"
    ).astype("Int64")

    print("========== DATASET SIZES ==========")

    print("Airbnb rows:", len(airbnb))
    print("Bond rows:", len(bonds))
    print("Merged rows:", len(merged))

    print("\n========== BOND DUPLICATES ==========")

    duplicate_bonds = bonds.duplicated(
        ["sa2_code", "year_quarter"]
    ).sum()

    print(
        "Duplicate SA2-quarter pairs:",
        duplicate_bonds
    )

    # --------------------------------------------------
    # Recreate the merge for diagnostics
    # --------------------------------------------------

    comparison = airbnb.merge(
        bonds,
        on=["sa2_code", "year_quarter"],
        how="left",
        validate="many_to_one",
        indicator=True
    )

    print("\n========== MERGE RESULTS ==========")

    print(
        "Matched:",
        (comparison["_merge"] == "both").sum()
    )

    print(
        "Unmatched:",
        (comparison["_merge"] == "left_only").sum()
    )

    print("\n========== RESULTS BY QUARTER ==========")

    print(
        comparison.groupby(
            ["year_quarter", "_merge"],
            observed=True
        )
        .size()
        .unstack(fill_value=0)
    )

    # --------------------------------------------------
    # Find Airbnb SA2s missing from cleaned bonds
    # --------------------------------------------------

    airbnb_codes = set(
        airbnb["sa2_code"].dropna()
    )

    bond_codes = set(
        bonds["sa2_code"].dropna()
    )

    missing_codes = sorted(
        airbnb_codes - bond_codes
    )

    print("\n========== SA2 CODES MISSING FROM BONDS ==========")

    for code in missing_codes:
        print(int(code))

    print(
        "Number of missing SA2 codes:",
        len(missing_codes)
    )

    # --------------------------------------------------
    # Find biggest groups of unmatched Airbnb listings
    # --------------------------------------------------

    unmatched = comparison[
        comparison["_merge"] == "left_only"
    ].copy()

    print(
        "\n========== LARGEST UNMATCHED SA2 AREAS =========="
    )

    print(
        unmatched.groupby(
            [
                "year_quarter",
                "sa2_code",
                "sa2_name"
            ]
        )
        .size()
        .sort_values(ascending=False)
        .head(30)
    )


def main():
    check_merge()
    print("\nDiagnostics completed with no errors.")


if __name__ == "__main__":
    main()