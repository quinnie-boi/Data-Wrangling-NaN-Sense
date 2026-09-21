
import pandas as pd

# Open the existing Airbnb dataset
data = pd.read_csv("data/listings_25-10_26-06.csv")

# Check how many rows it contains
print("Total rows:", len(data))

# Check which locations are included
print("\nLocations:")
print(data["neighbourhood_group"].value_counts(dropna=False))

# Check missing values in important columns
print("\nMissing values:")
chch_data = data[data["neighbourhood_group"] == "Christchurch City"]

print(chch_data[["price", "latitude", "longitude"]].isna().sum())

print("Christchurch rows with a price:",
      chch_data["price"].notna().sum())

# Make a separate copy of the Christchurch data
cleaned_chch = chch_data.copy()

# Remove rows without a nightly price
cleaned_chch = cleaned_chch.dropna(subset=["price"])

# Remove unnecessary columns
cleaned_chch = cleaned_chch.drop(columns=[
    "Unnamed: 0",
    "name",
    "host_name",
    "neighbourhood_group",
    "minimum_nights",
    "reviews_per_month",
    "license"
])

# Save to a NEW file (do not overwrite the original)
cleaned_chch.to_csv(
    "data/chch_cleaned.csv",
    index=False
)

print("Cleaned Christchurch rows:", len(cleaned_chch))
print("Cleaned file saved!")
print("\nColumns in cleaned Airbnb dataset:")
print(cleaned_chch.columns.tolist())

print("\nAirbnb collection months:")
print(
    cleaned_chch[["year", "month"]]
    .drop_duplicates()
    .sort_values(["year", "month"])
    .to_string(index=False)
)

print("\nMonths in the ORIGINAL Christchurch data:")

print(
    chch_data[["year", "month"]]
    .value_counts()
    .sort_index()
)

print("\nMissing prices in each month:")

print(
    chch_data.groupby(["year", "month"])["price"]
    .agg(
        total_rows="size",
        missing_prices=lambda prices: prices.isna().sum(),
        available_prices="count"
    )
)

# Keep all Christchurch listings for property counts
chch_all = chch_data.drop(columns=[
    "Unnamed: 0",
    "name",
    "host_name",
    "neighbourhood_group",
    "minimum_nights",
    "reviews_per_month",
    "license"
])

# Save a separate file without deleting missing prices
chch_all.to_csv(
    "data/chch_all_listings.csv",
    index=False
)

print("All Christchurch listings saved:", len(chch_all))

# Check the rental bond dataset
bond_data = pd.read_csv("data/quarterly_2025_2026.csv")

print("\nRENTAL BOND DATA")
print("Total rows:", len(bond_data))

print("\nColumn names:")
print(bond_data.columns.tolist())

print("\nFirst 5 rows:")
print(bond_data.head().to_string(index=False))

# Check which dates are available in the rental bond data
print("\nRENTAL BOND DATES")

print(
    bond_data["TimeFrame"]
    .drop_duplicates()
    .sort_values()
    .tail(12)
    .to_string(index=False)
)

# Make a separate copy of the rental bond data
cleaned_bond = bond_data.copy()

# Convert the TimeFrame column into dates
cleaned_bond["TimeFrame"] = pd.to_datetime(
    cleaned_bond["TimeFrame"]
)

# Keep quarters from October 2025 onward
cleaned_bond = cleaned_bond[
    cleaned_bond["TimeFrame"] >= "2025-10-01"
].copy()

print("\nBOND DATA AFTER DATE FILTERING")
print("Rows remaining:", len(cleaned_bond))
print(cleaned_bond["TimeFrame"].value_counts().sort_index())

# Remove bond rows without a usable location ID
before = len(cleaned_bond)

cleaned_bond = cleaned_bond.dropna(
    subset=["Location Id"]
).copy()

cleaned_bond = cleaned_bond[
    cleaned_bond["Location Id"] != -99
].copy()

print("\nBOND LOCATION CLEANING")
print("Rows before:", before)
print("Rows removed:", before - len(cleaned_bond))
print("Rows remaining:", len(cleaned_bond))

# Remove rows without a median rental price
before = len(cleaned_bond)

cleaned_bond = cleaned_bond.dropna(
    subset=["Median Rent"]
).copy()

print("\nBOND RENT CLEANING")
print("Rows before:", before)
print("Rows removed:", before - len(cleaned_bond))
print("Rows remaining:", len(cleaned_bond))

# Check the bedroom categories in the bond data
print("\nBOND BEDROOM CATEGORIES")
print(
    cleaned_bond["Number Of Beds"]
    .value_counts(dropna=False)
    .sort_index()
)

# Group individual bedroom counts of 5 or more into "5+"
cleaned_bond["Number Of Beds"] = cleaned_bond["Number Of Beds"].replace({
    "5": "5+",
    "6": "5+",
    "9": "5+"
})

print("\nBEDROOM CATEGORIES AFTER CLEANING")
print(
    cleaned_bond["Number Of Beds"]
    .value_counts(dropna=False)
    .sort_index()
)

# Save the cleaned rental bond data as a NEW file
cleaned_bond.to_csv(
    "data/bond_cleaned.csv",
    index=False
)

print("\nCLEANED BOND FILE SAVED")
print("Rows saved:", len(cleaned_bond))
print("File: data/bond_cleaned.csv")

# Get one Airbnb location for testing the Koordinates API
print("\nONE AIRBNB LOCATION")

print(
    cleaned_chch[["latitude", "longitude"]]
    .head(1)
    .to_string(index=False)
)

# Check whether our test SA2 code exists in the cleaned bond dataset
import pandas as pd

bond_check = pd.read_csv("data/bond_cleaned.csv")

test_area_code = 322200

matching_rows = bond_check[
    bond_check["Location Id"] == test_area_code
]

print("\nCHECK TEST AREA IN BOND DATA")
print("Area code:", test_area_code)
print("Matching bond rows:", len(matching_rows))
print(matching_rows[["TimeFrame", "Location Id", "Median Rent"]].head())

print("\nBOND RECORDS FOR TEST AREA")

print(
    matching_rows[
        ["TimeFrame", "Location Id", "Dwelling Type",
         "Number Of Beds", "Median Rent", "Active Bonds"]
    ].to_string(index=False)
)

print("\nOVERALL BOND RECORDS")

overall_bonds = bond_check[
    (bond_check["Dwelling Type"] == "ALL") &
    (bond_check["Number Of Beds"] == "ALL")
].copy()

print("Rows:", len(overall_bonds))

print(
    overall_bonds[
        ["TimeFrame", "Location Id", "Median Rent", "Active Bonds"]
    ].head(10).to_string(index=False)
)

print("\nCHECK DUPLICATE AREA AND QUARTER")

duplicates = overall_bonds.duplicated(
    subset=["TimeFrame", "Location Id"]
)

print("Duplicate rows:", duplicates.sum())
print("Unique area-quarter combinations:",
      overall_bonds[["TimeFrame", "Location Id"]].drop_duplicates().shape[0])

overall_bonds.to_csv(
    "data/bond_overall.csv",
    index=False
)

print("\nOverall bond file saved!")
print("File: data/bond_overall.csv")
print("Rows saved:", len(overall_bonds))





