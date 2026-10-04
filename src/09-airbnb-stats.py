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
    med_airbnb_price(326600, CLEANED_MERGED_DATASET_FILE)
)



def compare_central():
    jodi = pd.read_csv(JODI_SA2)
    new = pd.read_csv(CLEANED_MERGED_DATASET_FILE)

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


# compare_central()

def compare_dataset_location_population(filename = CLEANED_MERGED_DATASET_FILE):
    """
    print how many airbnb and rental properties are in each location
    filename: The merged airbnb and rental bonds dataset with sa2.
    """
    df = pd.read_csv(filename)
    #open csv using given filename
    # with open(df,'r') as property_data:
    #     # create necescarry dictionaries
    #     locate_airbnb_dict = {}
    #     locate_rental_dict = {}
    #     #loop through all listings and sort locations into different dict keys
    #     for property_listing in property_data:
    #         #split listing into list using .strip()
    #         property_listing = property_listing.strip().split(',')
    #         if property_listing[2] in locate_airbnb_dict:
    #             locate_airbnb_dict[property_listing[2]] += 1
    #         else:
    #             locate_airbnb_dict[property_listing[2]] = 1

    #         #simplify rental reigons this was added to put all (noth,west,south,east) variants into one location (remove if need be)
    #         splited_rental =  property_listing[-1].strip().split(' ')
    #         if splited_rental[-1] in ["North", "East", "South", "West"]:
    #             splited_rental.pop(-1)
    #         property_listing[-1] = " ".join(splited_rental)
    #         #(if needed remove up to here)

    #         if property_listing[-1] in locate_rental_dict:
    #             locate_rental_dict[property_listing[-1]] += 1
    #         else:
    #             locate_rental_dict[property_listing[-1]] = 1
    # # print out the location dicts:
    # print("Rental Locations:")
    # print(locate_rental_dict)
    # print("Airbnb Locations:")
    # print(locate_airbnb_dict)

    summary = (
        df.groupby("sa2_name")
        .agg(
            airbnb_listings=("id", "count"),
            active_bonds=("Active Bonds", "first"),
            total_bonds=("Total Bonds", "first")
        )
        .sort_values("airbnb_listings", ascending=False)
        .head()
    )

    print(summary)


def main():
    # Jodi Example to test for week 9 deliverable
    # median_price = med_airbnb_price(326600, CLEANED_AIRBNB_SA2_FILE)
    # print('#' * 10, 'Median Price', '#' * 10)
    # print(f"Median Airbnb price for Christchurch Central (SA2: 326600): ${median_price:.2f}\n\n")
    print("alex")
    compare_dataset_location_population()

if __name__ == "__main__":
    main()