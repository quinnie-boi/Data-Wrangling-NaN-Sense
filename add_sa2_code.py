import pandas as pd
import requests
import time
# Files for our Christchurch Airbnb project
INPUT_FILE = "data/chch_cleaned.csv"
OUTPUT_FILE = "data/chch_with_sa2.csv"

# Stats NZ Statistical Area 2 (2019) layer
LAYER_ID = 98970
API_URL = "https://datafinder.stats.govt.nz/services/query/v1/vector.json"

import os

API_KEY = "d20503a1cddf4351b5cb2e12b60d636b"

# Test one Christchurch Airbnb location
params = {
    "key": API_KEY,
    "layer": LAYER_ID,
    "x": 172.6254,
    "y": -43.51149,
    "max_results": 3,
    "radius": 10000,
    "geometry": "false",
    "with_field_names": "true"
}

response = requests.get(API_URL, params=params, timeout=30)
response.raise_for_status()

result = response.json()
features = result["vectorQuery"]["layers"][str(LAYER_ID)]["features"]

# Select the area containing our location
matching = [feature for feature in features if feature.get("distance") == 0]

if matching:
    area = matching[0]["properties"]
    print("SA2 code:", area["SA22019_V1_00"])
    print("Area name:", area["SA22019_V1_00_NAME"])
else:
    print("No matching SA2 area found.")

# Load our cleaned Christchurch Airbnb dataset
airbnb = pd.read_csv(INPUT_FILE)

print("Total Airbnb rows:", len(airbnb))
print("Columns:", airbnb.columns.tolist())

# Count different Airbnb locations
unique_locations = airbnb[["latitude", "longitude"]].drop_duplicates()

print("Unique locations:", len(unique_locations))

# Check the first unique location
first_location = unique_locations.iloc[0]

print("First latitude:", first_location["latitude"])
print("First longitude:", first_location["longitude"])

def get_sa2_code(latitude, longitude):
    params = {
        "key": API_KEY,
        "layer": LAYER_ID,
        "x": longitude,
        "y": latitude,
        "max_results": 3,
        "radius": 10000,
        "geometry": "false"
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    features = response.json()["vectorQuery"]["layers"][str(LAYER_ID)]["features"]

    for feature in features:
        if feature.get("distance") == 0:
            return feature["properties"]["SA22019_V1_00"]

    return None


# Test our function using the first Airbnb location
test_code = get_sa2_code(
    first_location["latitude"],
    first_location["longitude"]
)

print("SA2 code from function:", test_code)

# Test the function with three unique Airbnb locations
for index, location in unique_locations.head(3).iterrows():
    code = get_sa2_code(
        location["latitude"],
        location["longitude"]
    )
    print("Location", index, "SA2 code:", code)

# File to save our progress while looking up SA2 codes
CHECKPOINT_FILE = "data/sa2_lookup_progress.csv"

print("Checkpoint file:", CHECKPOINT_FILE)

# Create an empty checkpoint if one does not already exist
if not os.path.exists(CHECKPOINT_FILE):
    pd.DataFrame(
        columns=["latitude", "longitude", "sa2_code"]
    ).to_csv(CHECKPOINT_FILE, index=False)
    print("New checkpoint created.")
else:
    print("Existing checkpoint found.")

# Test saving three SA2 lookups to our checkpoint
checkpoint = pd.read_csv(
    CHECKPOINT_FILE,
    dtype={"sa2_code": "string"}
)

if checkpoint.empty:
    test_results = []

    for _, location in unique_locations.head(3).iterrows():
        code = get_sa2_code(
            location["latitude"],
            location["longitude"]
        )

        test_results.append({
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "sa2_code": code
        })

    pd.DataFrame(test_results).to_csv(CHECKPOINT_FILE, index=False)
    print("Saved three locations to checkpoint.")
else:
    print("Checkpoint already contains", len(checkpoint), "locations.")

# Check the saved checkpoint
saved_progress = pd.read_csv(
    CHECKPOINT_FILE,
    dtype={"sa2_code": "string"}
)

print("Saved locations:", len(saved_progress))
print(saved_progress.head(3).to_string(index=False))

# Check which locations still need an SA2 lookup
locations_to_check = unique_locations.merge(
    saved_progress[["latitude", "longitude"]],
    on=["latitude", "longitude"],
    how="left",
    indicator=True
)

remaining_locations = locations_to_check[
    locations_to_check["_merge"] == "left_only"
]

print("Locations already saved:", len(saved_progress))
print("Locations still to look up:", len(remaining_locations))



# Confirm how many locations are saved
updated_progress = pd.read_csv(
    CHECKPOINT_FILE,
    dtype={"sa2_code": "string"}
)

print("Total saved locations:", len(updated_progress))

# Look up the remaining locations and save progress

for number, (_, location) in enumerate(remaining_locations.iterrows(), start=1):


    latitude = location["latitude"]
    longitude = location["longitude"]

    try:
        code = get_sa2_code(latitude, longitude)

        # Save this result immediately
        pd.DataFrame([{
            "latitude": latitude,
            "longitude": longitude,
            "sa2_code": code
        }]).to_csv(
            CHECKPOINT_FILE,
            mode="a",
            header=False,
            index=False
        )

        print(f"Saved {number}/{len(remaining_locations)}: SA2 {code}")

        # Small pause between API requests
        time.sleep(0.2)

    except requests.RequestException as error:
        print(f"API request failed at location {number}: {type(error).__name__}")
        print("Progress up to this point has been saved. Run the script again to resume.")
        break

print("Lookup run finished.")


