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
import time
import pandas as pd

from constants import (
    CLEANED_AIRBNB_FILE,
    CLEANED_AIRBNB_SA2_FILE
)


# ---------------------------------------------------------------------------
# API configuration
# ---------------------------------------------------------------------------

LAYER_ID = 98970

API_URL = (
    "https://datafinder.stats.govt.nz/"
    "services/query/v1/vector.json?"
)

SA2_CODE_COLUMN = "sa2_code"
SA2_NAME_COLUMN = "sa2_name"

QUERY_MAX_RESULTS = 1
QUERY_RADIUS_METRES = 500
QUERY_GEOMETRY = "false"
QUERY_WITH_FIELD_NAMES = "true"


# ---------------------------------------------------------------------------
# API query
# ---------------------------------------------------------------------------

def query_sa2(args):
    """
    Query the Stats NZ API for a latitude and longitude pair.

    Retries temporary network failures up to three times.

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

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            with urllib.request.urlopen(
                url,
                timeout=60
            ) as response:

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

            # Ignore nearby polygons that do not contain the point
            if feature.get("distance", -1) > 0:
                return None, None

            properties = feature.get(
                "properties",
                {}
            )

            return (
                properties.get("SA22019_V1_00_NAME"),
                properties.get("SA22019_V1_00"),
            )

        except Exception as exc:

            print(
                f"Query attempt {attempt}/{max_attempts} failed "
                f"for ({latitude}, {longitude}): {exc}"
            )

            if attempt < max_attempts:
                time.sleep(2)

    print(
        f"All query attempts failed for "
        f"({latitude}, {longitude})"
    )

    return None, None


# ---------------------------------------------------------------------------
# Test API
# ---------------------------------------------------------------------------

def test_single_query(df, api_key):
    """
    Test the API lookup using the first Airbnb row.

    This prevents processing the entire dataset if the API
    key, layer, or query is not working.
    """

    row = df.iloc[0]

    result = query_sa2(
        (
            row["latitude"],
            row["longitude"],
            api_key,
        )
    )

    print("Test query result:", result)

    return result


# ---------------------------------------------------------------------------
# Add SA2 information
# ---------------------------------------------------------------------------

def add_sa2_data(df, api_key):
    """
    Query SA2 names and codes for all Airbnb observations.
    """

    tasks = [
        (
            row.latitude,
            row.longitude,
            api_key,
        )
        for row in df.itertuples(index=False)
    ]

    # Limit concurrent requests
    worker_count = 4

    with mp.Pool(worker_count) as pool:
        results = pool.map(
            query_sa2,
            tasks
        )

    df[
        [
            SA2_NAME_COLUMN,
            SA2_CODE_COLUMN
        ]
    ] = pd.DataFrame(
        results,
        index=df.index
    )

    missing_count = (
        df[SA2_CODE_COLUMN]
        .isna()
        .sum()
    )

    matched_count = (
        len(df) - missing_count
    )

    print(
        f"Rows with an SA2 match: "
        f"{matched_count}"
    )

    print(
        f"Rows without an SA2 match: "
        f"{missing_count}"
    )

    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """
    Add SA2 information to the cleaned Airbnb dataset
    and save the resulting CSV.
    """

    # API key should be supplied as a command-line argument
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python src/03-airbnb-sa2.py API_KEY"
        )
        sys.exit(1)

    api_key = sys.argv[1]

    # Read cleaned Airbnb data
    df = pd.read_csv(
        CLEANED_AIRBNB_FILE
    )

    # Check required coordinate columns
    required_columns = {
        "latitude",
        "longitude"
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if df.empty:
        raise ValueError(
            "The cleaned Airbnb dataset is empty."
        )

    # Test API before processing everything
    print("Running test query...")

    test_result = test_single_query(
        df,
        api_key
    )

    if test_result == (None, None):
        print(
            "Test query did not return "
            "an SA2 match."
        )

        print(
            "Check the API key, layer ID, "
            "API permissions, and coordinates."
        )

        sys.exit(1)

    print("Test query successful.")
    print("Processing all rows...")

    # Add SA2 information
    df = add_sa2_data(
        df,
        api_key
    )

    # Store SA2 codes as nullable integers
    df[SA2_CODE_COLUMN] = pd.to_numeric(
        df[SA2_CODE_COLUMN],
        errors="coerce"
    ).astype("Int64")

    # Save completed dataset
    df.to_csv(
        '/out/test_sa2.csv',
        index=False
    )

    print(
        f"Saved output to: "
        f"{"test_sa2.csv"}"
    )

    print("No errors")


if __name__ == "__main__":
    main()