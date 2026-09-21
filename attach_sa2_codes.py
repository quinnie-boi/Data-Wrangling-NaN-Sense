import pandas as pd

# Our existing files
AIRBNB_FILE = "data/chch_cleaned.csv"
SA2_FILE = "data/sa2_lookup_progress.csv"

# The updated file we will create
OUTPUT_FILE = "data/chch_with_sa2.csv"

# Read both datasets
airbnb = pd.read_csv(AIRBNB_FILE)
sa2_lookup = pd.read_csv(SA2_FILE, dtype={"sa2_code": "string"})

print("Airbnb rows:", len(airbnb))
print("Saved SA2 locations:", len(sa2_lookup))
print("Missing SA2 codes:", sa2_lookup["sa2_code"].isna().sum())
print("Duplicate coordinates:", sa2_lookup.duplicated(["latitude", "longitude"]).sum())

# Attach SA2 codes using latitude and longitude
airbnb_with_sa2 = airbnb.merge(
    sa2_lookup[["latitude", "longitude", "sa2_code"]],
    on=["latitude", "longitude"],
    how="left",
    validate="many_to_one"
)

# Check the result before saving
print("Rows after merging:", len(airbnb_with_sa2))
print("Rows without SA2 code:", airbnb_with_sa2["sa2_code"].isna().sum())
print("New column:", airbnb_with_sa2.columns[-1])

# Save the Airbnb dataset with its SA2 codes
airbnb_with_sa2.to_csv(OUTPUT_FILE, index=False)

print("Updated Airbnb dataset saved:", OUTPUT_FILE)
