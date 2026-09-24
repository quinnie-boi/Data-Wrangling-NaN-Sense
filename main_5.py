import pandas as pd
import os
from constants import AIRBNB_FILE_NAME, CLEANED_AIRBNB_FILE, CLEANED_BONDS_FILE, CLEANED_DIR, CLEANED_MERGED_DATASET_FILE

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



def merge_sa2_codes():
    """
    Merges the SA2_code column from Prasanthi's dataset uploaded to Trello
    in to our own pipeline. Saves the output to
    """
    sa2 = pd.read_csv("data/prasanthi_airbnb_with_sa2.csv")
    airbnb = pd.read_csv(CLEANED_AIRBNB_FILE)

    key = 'id'
    airbnb = pd.merge(airbnb, sa2[[key, 'sa2_code']], on = key, how = 'left'  )
    print(airbnb['sa2_code'].summary())
    print(sa2['sa2_code'].summary())

    airbnb.to_csv(CLEANED_AIRBNB_FILE.replace(".csv", "_sa2.csv"))

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



def merge_rental_bonds_and_chch_listings():
    """
    merges our rental bonds dataset with our listings dataset along
    the new sa2_code column.
    """
    # Written by Syamily :)
    # Tweaked by Quinn

    if os.path.exists(CLEANED_MERGED_DATASET_FILE):
        print('#'*10, 'INFO', '#'*10)
        print(f"Skipped merging files {CLEANED_MERGED_DATASET_FILE} already exists.\n\n")
        return

    # Read the datasets
    airbnb = pd.read_csv(
        CLEANED_AIRBNB_FILE.replace(".csv", "_with_sa2.csv"),
    )

    bond = pd.read_csv(CLEANED_BONDS_FILE)

    # Check the files before joining
    # print("Airbnb rows:", len(airbnb))
    # print("Bond rows:", len(bond))
    # print("Airbnb columns:\n ", ",\n  ".join(airbnb.columns.tolist()))
    # print("Bond columns:\n ", ",\n  ".join(bond.columns.tolist()))

    airbnb["listing_date"] = pd.to_datetime(
        airbnb.assign(
            year=airbnb["scrape_year"] + 2000,
            month=airbnb["scrape_month"],
            day=1
        )[["year", "month", "day"]]
    )

    # create a quarters column
    airbnb["quarter"] = airbnb["listing_date"].dt.to_period("Q")

    # Check the result
    # print(
    #     "chch listing dates:\n",
    #     airbnb["listing_date"]
    #     .drop_duplicates()
    #     .head()
    #     .to_string(index=False)
    # )

    # Prepare the Rental Bond columns for joining
    bond["quarter"] = pd.to_datetime(bond["TimeFrame"])

    # Make sure both datasets use the same area-code format
    if bond['sa2_code'].dtype !=  airbnb['sa2_code'].dtype:
        print(f"rental bonds has sa2_code dtype of {bond['sa2_code'].dtype}")
        print(f"      airbnb has sa2_code dtype of {airbnb['sa2_code'].dtype}")
        raise TypeError("err")


    # # Check that each area has only one Bond row per quarter
    # print("Bond duplicate area-quarter pairs:",
    #     bond.duplicated(["sa2_code", "quarter"]).sum())

    # print("Bond quarters:",
    #     bond["quarter"].drop_duplicates().tolist())

    # Join Airbnb with Rental Bond using area code and quarter
    # joined = airbnb.merge(
    #     bond,
    #     on=["sa2_code", "quarter"],
    #     how="left",
    #     validate="many_to_one",
    #     indicator=True
    # )
    joined = airbnb.merge(
        bond,
        on='sa2_code',
        how='left',
        indicator=True
    )

    # Check the result before saving
    print("Airbnb rows before join:", len(airbnb))
    print("Rows after join:", len(joined))
    print("Rows matched with Bond:", (joined["_merge"] == "both").sum())
    print("Rows without Bond match:", (joined["_merge"] == "left_only").sum())

    # Check the area-code values in both datasets
    # print("Airbnb SA2 examples:", airbnb["sa2_code"].head(5).tolist())
    # print("Bond SA2 examples:", bond["sa2_code"].head(5).tolist())

    # Check whether the same area codes appear in both datasets
    # common_codes = set(airbnb["sa2_code"]) & set(bond["sa2_code"])
    # print("Number of common area codes:", len(common_codes))

    # Check matched and unmatched rows by quarter
    # print("\nMatches by quarter:")
    # print(
    #     joined.groupby(["quarter", "_merge"], observed=True)
    #     .size()
    #     .unstack(fill_value=0)
    #     .to_string()
    # )

    # Remove the temporary column used to check matches
    joined = joined.drop(columns=["_merge"])

    # Save the joined dataset as a new CSV
    OUTPUT_FILE = CLEANED_MERGED_DATASET_FILE

    joined.to_csv(OUTPUT_FILE, index=False)

    print("Joined dataset saved:", OUTPUT_FILE)
    print("Final rows:", len(joined))


def prasanthi(df):
    """
    In which part of Christchurch can we observe the
    craziest (largest) gap between short- and long-term rental prices?
    """

    # 2. Calculate the nightly rate from your weekly column
    # Kate mentioned that the Geometric Mean Rent was a better price to analysis than the Median Rent
    # Make sure that the file column names are same as the ones noted here
    df["nightly_rental_rate"] = (df["Geometric Mean Rent"] / 7).round(2)

    # 3. Calculate the difference directly against the Airbnb price column row-by-row
    # Replace 'airbnb_price' with the exact name of the price column in your file
    df["price_difference"] = (df["price"] - df["nightly_rental_rate"]).round(2)

    # 4. View the updated data
    # print(df)

    ###I have checked the code upto this section###
    #####chch_airbnb_bond_joined.csv dataset does not contain sa2_names, we need it for this deliverable#####

    # 5. Calculate Mean Price Difference by SA2 Code
    mean_differences = (
        df.groupby(["sa2_code", "sa2_name"])["price_difference"]
        .mean()
        .round(2)
        .reset_index()
    )
    mean_differences = mean_differences.rename(
        columns={"price_difference": "mean_price_difference"}
    )

    # 6. Sort in Descending Order based on Mean Difference
    mean_differences_sorted = mean_differences.sort_values(
        by="mean_price_difference", ascending=False
    )

    # Optional: Adjust Pandas print display options so PyCharm's console doesn't truncate text
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)

    # --- 7. Print the Table ---
    print("--- sa2 Code Areas Ranked by Mean Price Difference (Descending) ---")
    print(mean_differences_sorted.head().to_string(index=False))


merge_rental_bonds_and_chch_listings()
prasanthi(pd.read_csv(CLEANED_MERGED_DATASET_FILE))

# Jodi Example to test for week 9 deliverable
median_price = med_airbnb_price(326600, CLEANED_MERGED_DATASET_FILE)
print('#'*10, 'Median Price', '#'*10)
print(f"Median Airbnb price for Christchurch Central (SA2: 326600): ${median_price:.2f}\n\n")


print('#'*10, 'Compare airbnb listings and rental bonds', '#'*10)
compare_dataset_location_population(CLEANED_MERGED_DATASET_FILE)
# Example output
# sa2_code                           sa2_name  mean_price_difference
# 317400.0                          Northwood                 512.73
# 326600.0               Christchurch Central                 394.68
# 323600.0                       Wigram South                 373.30
# 316800.0                         Clearwater                 363.30
# 331900.0                   Heathcote Valley                 334.17
# 320800.0                      Bryndwr South                 289.86
# 316600.0                          Yaldhurst                 287.19
# 332700.0                             Sumner                 286.02
# 322800.0                        Wigram West                 242.64
# 322600.0                           Holmwood                 222.06
# 328800.0                     Lancaster Park                 218.21
# 323900.0                     St Albans West                 215.57
# 325700.0          Christchurch Central-West                 215.33
# 320900.0                       Papanui East                 214.39
# 318100.0                          Templeton                 212.26
# 332100.0                          Redcliffs                 204.20
# 324400.0                    Riccarton South                 197.61
# 332900.0                    Diamond Harbour                 197.43
# 330500.0                             Ensors                 196.04
# 323000.0                           Merivale                 193.00
# 322100.0                            Malvern                 187.67
# 322300.0                     Sockburn South                 185.29
# 327000.0          Christchurch Central-East                 183.41
# 319400.0                      Papanui North                 182.70
# 325800.0         Christchurch Central-North                 180.70
# 327300.0                     Halswell North                 178.97



# Example output with previous dataset
# --- sa2 Code Areas Ranked by Mean Price Difference (Descending) ---
# sa2_code                           sa2_name  mean_price_difference
#   326600               Christchurch Central                 361.05
#   316800                         Clearwater                 349.17
#   317400                          Northwood                 339.72
#   332700                             Sumner                 312.08
#   323600                       Wigram South                 286.96
#   320800                      Bryndwr South                 280.06
#   331900                   Heathcote Valley                 258.32
#   322600                           Holmwood                 244.70
#   322800                        Wigram West                 241.14
#   316600                          Yaldhurst                 240.11
#   331300                      Cashmere East                 238.85
#   324200                  Riccarton Central                 235.47
#   330500                             Ensors                 222.73
#   325700          Christchurch Central-West                 221.88
#   323000                           Merivale                 209.05
#   322100                            Malvern                 208.93
#   323900                     St Albans West                 206.83
#   328800                     Lancaster Park                 203.73
#   324400                    Riccarton South                 194.50
#   326100                     Addington West                 193.71
#   332100                          Redcliffs                 193.71
#   321400                            Strowan                 190.05
#   326800 Richmond South (Christchurch City)                 187.19
#   327000          Christchurch Central-East                 186.38
#   332400                       Clifton Hill                 185.99
