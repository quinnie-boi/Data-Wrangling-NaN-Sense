import pandas as pd

# Files prepared for our project
AIRBNB_FILE = "data/chch_with_sa2.csv"
BOND_FILE = "data/bond_overall.csv"

# Read the datasets
airbnb = pd.read_csv(
    AIRBNB_FILE,
    dtype={"sa2_code": "string"}
)

bond = pd.read_csv(BOND_FILE)

# Check the files before joining
print("Airbnb rows:", len(airbnb))
print("Bond rows:", len(bond))
print("Airbnb columns:", airbnb.columns.tolist())
print("Bond columns:", bond.columns.tolist())

# Convert two-digit years (25, 26) into four-digit years (2025, 2026)
airbnb["listing_date"] = pd.to_datetime(
    airbnb[["year", "month"]]
    .assign(year=lambda df: df["year"] + 2000, day=1)
)


# Convert each month to the start of its quarter
airbnb["quarter"] = (
    airbnb["listing_date"]
    .dt.to_period("Q")
    .dt.start_time
)

# Check the result
print(
    airbnb[["year", "month", "quarter"]]
    .drop_duplicates()
    .sort_values(["year", "month"])
    .to_string(index=False)
)

# Prepare the Rental Bond columns for joining
bond["quarter"] = pd.to_datetime(bond["TimeFrame"])

# Make sure both datasets use the same area-code format

bond["sa2_code"] = pd.to_numeric(
    bond["Location Id"]
).astype("Int64").astype("string")


# Check that each area has only one Bond row per quarter
print("Bond duplicate area-quarter pairs:",
      bond.duplicated(["sa2_code", "quarter"]).sum())

print("Bond quarters:",
      bond["quarter"].drop_duplicates().sort_values().tolist())

# Join Airbnb with Rental Bond using area code and quarter
joined = airbnb.merge(
    bond,
    on=["sa2_code", "quarter"],
    how="left",
    validate="many_to_one",
    indicator=True
)

# Check the result before saving
print("Airbnb rows before join:", len(airbnb))
print("Rows after join:", len(joined))
print("Rows matched with Bond:", (joined["_merge"] == "both").sum())
print("Rows without Bond match:", (joined["_merge"] == "left_only").sum())

# Check the area-code values in both datasets
print("Airbnb SA2 examples:", airbnb["sa2_code"].head(5).tolist())
print("Bond SA2 examples:", bond["sa2_code"].head(5).tolist())

# Check whether the same area codes appear in both datasets
common_codes = set(airbnb["sa2_code"]) & set(bond["sa2_code"])
print("Number of common area codes:", len(common_codes))

# Check matched and unmatched rows by quarter
print("\nMatches by quarter:")
print(
    joined.groupby(["quarter", "_merge"], observed=True)
    .size()
    .unstack(fill_value=0)
    .to_string()
)

# Remove the temporary column used to check matches
joined = joined.drop(columns=["_merge"])

# Save the joined dataset as a new CSV
OUTPUT_FILE = "data/chch_airbnb_bond_joined.csv"

joined.to_csv(OUTPUT_FILE, index=False)

print("Joined dataset saved:", OUTPUT_FILE)
print("Final rows:", len(joined))

