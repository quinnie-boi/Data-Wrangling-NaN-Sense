import pandas as pd

# Our existing joined Airbnb and rental bond dataset
JOINED_FILE = "data/chch_airbnb_bond_joined.csv"

# Downloaded Stats NZ SA2 2019 dataset
SA2_FILE = "data/statistical-area-2-higher-geographies-2019-generalised.csv"

# Read the files
joined = pd.read_csv(JOINED_FILE, dtype={"sa2_code": "string"})

sa2 = pd.read_csv(
    SA2_FILE,
    usecols=["SA22019_V1_00", "SA22019_V1_00_NAME"],
    dtype={"SA22019_V1_00": "string"}
)

# Check the data before joining
print("Joined dataset rows:", len(joined))
print("SA2 reference rows:", len(sa2))
print("SA2 reference columns:", sa2.columns.tolist())
print("Duplicate SA2 codes:", sa2["SA22019_V1_00"].duplicated().sum())
print("Missing SA2 names:", sa2["SA22019_V1_00_NAME"].isna().sum())
# Rename the Stats NZ columns to match our project
sa2 = sa2.rename(columns={
    "SA22019_V1_00": "sa2_code",
    "SA22019_V1_00_NAME": "sa2_name"
})

# Add the area names while keeping all existing Airbnb rows
updated = joined.merge(
    sa2,
    on="sa2_code",
    how="left",
    validate="many_to_one"
)

# Check the result before saving
print("Rows before adding names:", len(joined))
print("Rows after adding names:", len(updated))
print("Missing SA2 names:", updated["sa2_name"].isna().sum())

print("\nSA2 code and name examples:")
print(updated[["sa2_code", "sa2_name"]].drop_duplicates().head(10).to_string(index=False))
# Save the joined dataset with SA2 names
OUTPUT_FILE = "data/chch_airbnb_bond_with_sa2_names.csv"

updated.to_csv(OUTPUT_FILE, index=False)

print("\nUpdated dataset saved:", OUTPUT_FILE)
print("Final rows:", len(updated))