import pandas as pd

from constants import AIRBNB_FILE_NAME, CLEANED_AIRBNB_FILE, CLEANED_BONDS_FILE, CLEANED_MERGED_DATASET_FILE

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


def merge_rental_bonds_and_chch_listings():
    """
    merges our rental bonds dataset with our listings dataset along
    the new sa2_code column.
    """
    # Waiting on Syamily :)
    # quick tmp fix
    # add sa2_name column by merging
    sa2 = pd.read_csv("data/prasanthi_airbnb_with_sa2.csv", usecols=['sa2_code', 'sa2_name'])
    merged = pd.read_csv(CLEANED_MERGED_DATASET_FILE)

    # match datatypes
    # they are object and int64 by defaultw
    sa2['sa2_code'] = sa2['sa2_code'].astype(str)
    merged['sa2_code'] = merged['sa2_code'].astype(str)

    if 'sa2_names' in merged.columns:
        print(f"The dataset file: {CLEANED_MERGED_DATASET_FILE} already contains sa2 code names")
    else:
        # print(merged.columns.intersection(sa2.columns))

        merged = merged.merge( sa2, on='sa2_code', how="left")
        merged.to_csv(CLEANED_MERGED_DATASET_FILE)




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
    print(df)

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
    print(mean_differences_sorted.to_string(index=False))


merge_rental_bonds_and_chch_listings()
prasanthi(pd.read_csv(CLEANED_MERGED_DATASET_FILE))

# Example output
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