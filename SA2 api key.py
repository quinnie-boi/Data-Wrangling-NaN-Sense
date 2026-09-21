#Testing for one coordinate

import requests

url = "https://datafinder.stats.govt.nz/services/query/v1/vector.json?key=0deb3efae8f6415d9f1d7bdc3522ab85&layer=123515&x=[x]&y=[y]&max_results=3&radius=10000&geometry=true&with_field_names=true"
payload = {
    "key": "0deb3efae8f6415d9f1d7bdc3522ab85",
    "layer": 123515,
    "x": 172.57088,  # Pass as a float number, not a string "172.6206"
    "y": -43.47002,  # Pass as a float number
    "radius": 0,
    "geometry": "false",
}
response = requests.get(url, params=payload)
print(response.json())


#Testing for Tenancy Cleaned Data Set

import time
import pandas as pd
import requests

# 1. Configuration Settings
API_KEY = "0deb3efae8f6415d9f1d7bdc3522ab85"
# alex API key 23bc2284145b4baa940e1c4c067cefd8
LAYER_ID = 123515  # Statistical Area 2 2026 layer
INPUT_FILE = "data/chcListingsCutNoDup.csv" # <- Prasanthi & Robbies Airbnb data
OUTPUT_FILE = "data/dataset_with_sa2.csv"

# CORRECT API URL (Updated from general stats.govt.nz domain)
API_URL = "https://datafinder.stats.govt.nz/services/query/v1/vector.json?key=0deb3efae8f6415d9f1d7bdc3522ab85&layer=123515&x=[x]&y=[y]&max_results=3&radius=10000&geometry=true&with_field_names=true"
# AlEX API URL - SA2 2019 <- if we want to change it to the SA2 2019 version and not the 2026 version
API_ALEX = 'https://datafinder.stats.govt.nz/layer/98779-statistical-area-2-higher-geographies-2019-generalised/'

def get_sa2_data(longitude, latitude):
    """Queries Stats NZ API to discover which SA2 polygon contains the point."""
    payload = {
        "key": API_KEY,
        "layer": LAYER_ID,
        "x": float(longitude),  # Explicitly force float numbers
        "y": float(latitude),  # Explicitly force float numbers
        "radius": 0,  # Exact point-in-polygon lookup
        "geometry": "false",  # Exclude heavy shape data for speed
    }

    try:
        response = requests.get(API_URL, params=payload, timeout=10)

        # Handle rate limiting (HTTP 429 Too Many Requests)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            print(f"⚠️ Rate limited. Pausing for {retry_after} seconds...")
            time.sleep(retry_after)
            return get_sa2_data(longitude, latitude)  # Retry the query

        # Process a successful matching record
        if response.status_code == 200:
            data = response.json()
            # Navigate into the JSON structure to get attributes
            if "vectorQuery" in data and data["vectorQuery"]["layers"]:
                layer_data = data["vectorQuery"]["layers"][str(LAYER_ID)]
                if layer_data and "features" in layer_data:
                    # Get the closest/exact overlapping polygon features
                    properties = layer_data["features"][0]["properties"]
                    return {
                        "sa2_code": properties.get("SA22026_V1_00"),
                        "sa2_name": properties.get("SA22026_V1_00_NAME"),
                    }

            return {"sa2_code": "NOT_FOUND", "sa2_name": "Outside Boundaries"}

        print(f"❌ HTTP Error {response.status_code} for point ({longitude}, {latitude})")
        return {"sa2_code": "ERROR", "sa2_name": f"HTTP_{response.status_code}"}

    except Exception as e:
        print(f"💥 Request failed for point ({longitude}, {latitude}): {str(e)}")
        return {"sa2_code": "EXCEPTION", "sa2_name": str(e)}


# 2. Main Execution Pipeline
def main():
    print(f"📖 Loading input dataset: {INPUT_FILE}...")
    # Read your cleaned data (ensure names match your actual CSV columns)
    df = pd.read_csv(INPUT_FILE)

    sa2_codes = []
    sa2_names = []

    total_rows = len(df)
    print(f"🚀 Processing {total_rows} locations against Stats NZ spatial layers...")

    for index, row in df.iterrows():
        # EXTRACT YOUR COORDINATE COLUMNS HERE
        lon = row["longitude"]
        lat = row["latitude"]

        # Call the API function
        result = get_sa2_data(lon, lat)

        # Track the returned attributes
        sa2_codes.append(result["sa2_code"])
        sa2_names.append(result["sa2_name"])

        # Progress tracking & Console logging
        if (index + 1) % 10 == 0 or (index + 1) == total_rows:
            print(f"⏳ Processed {index + 1}/{total_rows} rows...")

        # Courteous pacing to avoid server-side defensive blocks
        time.sleep(0.1)

    # 3. Append results and save
    df["sa2_code"] = sa2_codes
    df["sa2_name"] = sa2_names

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"🎉 Complete! Enriched dataset safely exported to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
