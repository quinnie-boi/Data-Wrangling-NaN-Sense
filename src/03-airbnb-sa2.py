"""
Add SA2 2019 area codes and names to the cleaned Airbnb dataset.

Usage:
    python src/03-airbnb-sa2.py API_KEY
"""
import json
import multiprocessing as mp
import sys
import urllib.parse
import urllib.request

import pandas as pd

from constants import CLEANED_AIRBNB_FILE, CLEANED_AIRBNB_SA2_FILE


LAYER_ID = 98970

SA2_CODE_COLUMN = "sa2_code"
SA2_NAME_COLUMN = "sa2_name"

QUERY_MAX_RESULTS = 1
QUERY_RADIUS_METRES = 500
QUERY_GEOMETRY = "false"
QUERY_WITH_FIELD_NAMES = "true"

API_URL = "https://datafinder.stats.govt.nz/services/query/v1/vector.json?"



def query_sa2(args):
    """
    Query the Stats NZ API for a latitude and longitude pair.

    Returns (sa2_name, sa2_code) when the point falls within
    the returned SA2 polygon, otherwise returns (None, None).
    """

    latitude, longitude, api_key = args

    url = API_URL + urllib.parse.urlencode(
        {
            "key": api_key,
            "layer": LAYER_ID,
            "x": longitude,
            "y": latitude,
            "max_results": QUERY_MAX_RESULTS,
            "radius": QUERY_RADIUS_METRES,
            "geometry": QUERY_GEOMETRY,
            "with_field_names": QUERY_WITH_FIELD_NAMES,
        }
    )

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        features = (
            data.get("vectorQuery", {})
            .get("layers", {})
            .get(str(LAYER_ID), {})
            .get("features", [])
        )

        if not features:
            return None, None

        feature = features[0]

        # Ignore nearby polygons that don't contain the point
        if feature.get("distance", -1) > 0:
            return None, None

        properties = feature.get("properties", {})

        return (
            properties.get("SA22019_V1_00_NAME"),
            properties.get("SA22019_V1_00"),
        )

    except Exception as exc:
        print(
            f"Failed query for ({latitude}, {longitude}): {exc}"
        )
        return None, None


def test_single_query(df, api_key):
    """Test the API lookup on the first row."""

    row = df.iloc[0]

    result = query_sa2(
        (
            row["latitude"],
            row["longitude"],
            api_key,
        )
    )

    print(f"Test query result: {result}")

    return result


def add_sa2_data(df, api_key):
    """Add SA2 names and codes to the dataframe."""

    tasks = [
        (
            row.latitude,
            row.longitude,
            api_key,
        )
        for row in df.itertuples(index=False)
    ]

    # Keep concurrent API requests relatively low
    worker_count = 4

    with mp.Pool(worker_count) as pool:
        results = pool.map(query_sa2, tasks)

    df[[SA2_NAME_COLUMN, SA2_CODE_COLUMN]] = pd.DataFrame(
        results,
        index=df.index,
    )

    missing_count = df[SA2_CODE_COLUMN].isna().sum()

    print(f"Rows without an SA2 match: {missing_count}")
    print(f"Rows with an SA2 match: {len(df) - missing_count}")

    return df


def main():
    """Add SA2 information to the cleaned Airbnb dataset."""

    if len(sys.argv) != 2:
        print(
            "Usage: python src/03-airbnb-sa2.py API_KEY"
        )
        sys.exit(1)

    api_key = sys.argv[1]

    df = pd.read_csv(CLEANED_AIRBNB_FILE)

    required_columns = {"latitude", "longitude"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    print("Running test query...")

    test_result = test_single_query(df, api_key)

    if test_result == (None, None):
        print("Test query did not return an SA2 match.")
        print("Check the API key, layer ID, and coordinates.")
        sys.exit(1)

    print("Processing all rows...")

    df = add_sa2_data(df, api_key)

    # Store SA2 codes as nullable integers
    df[SA2_CODE_COLUMN] = pd.to_numeric(
        df[SA2_CODE_COLUMN],
        errors="coerce"
    ).astype("Int64")

    df.to_csv(
        CLEANED_AIRBNB_SA2_FILE,
        index=False
    )
    print(f"Saved output to {CLEANED_AIRBNB_SA2_FILE}")



if __name__ == "__main__":
    main()