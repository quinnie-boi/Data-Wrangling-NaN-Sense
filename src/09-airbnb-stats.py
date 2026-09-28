import pandas as pd
import os

from pandas import read_csv

from constants import CLEANED_AIRBNB_SA2_FILE, CLEANED_BONDS_FILE, CLEANED_MERGED_DATASET_FILE, JODI_SA2

def med_airbnb_price(location_id, filename):
    """Returns the median Airbnb price in a dataset for a given location,
    excludes blank or missing prices.
    Written by Jodi
    """

    #Loads dataset
    df = pd.read_csv(filename)

    #Filters to the specified sa2_code associated to the location_id parameter (e.g. 326600)
    df = df[df["sa2_code"] == location_id]

    #Pandas median() function ignores existing Not-a-Number (NaN) values, but will not convert blanks or text into NaN.
    #The entire price column appears numeric, so this line is likely not necessary, but if you get an error, use the
    # line below to convert non-numeric price entries to NaN so they are also excluded from the calculation.

    #df["price"] = pd.to_numeric(df["price"], errors="coerce")

    #Returns median price
    return df["price"].median()

print(
    "Jodi median:",
    med_airbnb_price(326600, JODI_SA2)
)

print(
    "New median:",
    med_airbnb_price(326600, CLEANED_AIRBNB_SA2_FILE)
)

def compare_central():
    jodi = pd.read_csv(JODI_SA2)
    new = pd.read_csv(CLEANED_AIRBNB_SA2_FILE)

    jodi = jodi[jodi["sa2_code"] == 326600].copy()
    new = new[new["sa2_code"] == 326600].copy()

    print("\n========== JODI ==========")
    print("Rows:", len(jodi))
    print("Unique IDs:", jodi["id"].nunique())
    print("Median:", jodi["price"].median())

    print("\n========== NEW ==========")
    print("Rows:", len(new))
    print("Unique IDs:", new["id"].nunique())
    print("Median:", new["price"].median())

    jodi_ids = set(jodi["id"])
    new_ids = set(new["id"])

    print("\n========== ID DIFFERENCES ==========")
    print("IDs only in Jodi:", len(jodi_ids - new_ids))
    print("IDs only in new:", len(new_ids - jodi_ids))
    print("IDs in both:", len(jodi_ids & new_ids))

compare_central()

extra_ids = new_ids - jodi_ids

extra_listings = new_central[
    new_central["id"].isin(extra_ids)
].copy()

print("\n========== EXTRA NEW LISTINGS ==========")
print("Unique extra listings:", extra_listings["id"].nunique())
print("Total extra observations:", len(extra_listings))

print(
    extra_listings[
        [
            "id",
            "price",
            "latitude",
            "longitude",
            "year_quarter",
            "sa2_code",
            "sa2_name"
        ]
    ]
    .sort_values(["id", "year_quarter"])
    .to_string(index=False)
)


def main():
    # Jodi Example to test for week 9 deliverable
    # median_price = med_airbnb_price(326600, CLEANED_AIRBNB_SA2_FILE)
    # print('#' * 10, 'Median Price', '#' * 10)
    # print(f"Median Airbnb price for Christchurch Central (SA2: 326600): ${median_price:.2f}\n\n")
    print("alex")


if __name__ == "__main__":
    main()