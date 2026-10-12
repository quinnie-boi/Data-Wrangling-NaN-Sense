"""
Deliverable 5

Add SA2 2019 area codes and names to the cleaned Airbnb dataset
using the Stats NZ Vector Query API.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request

import pandas as pd

from constants import (
    CLEANED_AIRBNB_FILE,
    CLEANED_AIRBNB_SA2_FILE
)


# ---------------------------------------------------------------------------
# API settings
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

MAX_RETRIES = 3
REQUEST_TIMEOUT = 60


# ---------------------------------------------------------------------------
# Query Stats NZ
# ---------------------------------------------------------------------------

def query_sa2(args):
    """
    Query the Stats NZ API for a latitude and longitude pair.

    Returns:
        (sa2_name, sa2_code)

    Returns (None, None) when no containing SA2 polygon is found.
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

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(
                url,
                timeout=REQUEST_TIMEOUT
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

            # A distance greater than zero means the returned
            # polygon is nearby but does not contain the point.
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
                f"Query attempt {attempt}/{MAX_RETRIES} failed "
                f"for ({latitude}, {longitude}): {exc}"
            )

            if attempt < MAX_RETRIES:
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
    """Test the API lookup using the first row."""

    row = df.iloc[0]

    result = query_sa2(
        (
            row["latitude"],
            row["longitude"],
            api_key,
        )
    )

    print("Test query result:")
    print(result)

    return result


# ---------------------------------------------------------------------------
# Add SA2 data
# ---------------------------------------------------------------------------

def add_sa2_data(df, api_key):
    """
    Add SA2 names and codes to the Airbnb data.

    Existing coordinate lookups are reused when available.
    Only previously unknown coordinates are sent to the API.
    """

    # ---------------------------------------------------------------
    # Load existing SA2 mappings if an output file already exists
    # ---------------------------------------------------------------

    try:
        old_data = pd.read_csv(
            CLEANED_AIRBNB_SA2_FILE,
            dtype={
                SA2_CODE_COLUMN: "string",
                SA2_NAME_COLUMN: "string"
            }
        )

        required_lookup_columns = {
            "latitude",
            "longitude",
            SA2_NAME_COLUMN,
            SA2_CODE_COLUMN
        }

        if required_lookup_columns.issubset(
            old_data.columns
        ):
            lookup = (
                old_data[
                    [
                        "latitude",
                        "longitude",
                        SA2_NAME_COLUMN,
                        SA2_CODE_COLUMN
                    ]
                ]
                .dropna(
                    subset=[SA2_CODE_COLUMN]
                )
                .drop_duplicates(
                    subset=[
                        "latitude",
                        "longitude"
                    ]
                )
                .copy()
            )

            print(
                f"Loaded {len(lookup)} existing "
                f"SA2 coordinate mappings."
            )

        else:
            lookup = pd.DataFrame(
                {
                    "latitude": pd.Series(
                        dtype="float64"
                    ),
                    "longitude": pd.Series(
                        dtype="float64"
                    ),
                    SA2_NAME_COLUMN: pd.Series(
                        dtype="string"
                    ),
                    SA2_CODE_COLUMN: pd.Series(
                        dtype="string"
                    ),
                }
            )

    except FileNotFoundError:
        lookup = pd.DataFrame(
            {
                "latitude": pd.Series(
                    dtype="float64"
                ),
                "longitude": pd.Series(
                    dtype="float64"
                ),
                SA2_NAME_COLUMN: pd.Series(
                    dtype="string"
                ),
                SA2_CODE_COLUMN: pd.Series(
                    dtype="string"
                ),
            }
        )

        print(
            "No existing SA2 file found. "
            "Starting with an empty lookup."
        )

    # ---------------------------------------------------------------
    # Work with unique coordinates
    # ---------------------------------------------------------------

    coordinates = (
        df[
            [
                "latitude",
                "longitude"
            ]
        ]
        .drop_duplicates()
        .copy()
    )

    # Add mappings we already know
    coordinates = coordinates.merge(
        lookup,
        on=[
            "latitude",
            "longitude"
        ],
        how="left",
        validate="one_to_one"
    )

    # Explicitly use strings while combining API results
    coordinates[SA2_NAME_COLUMN] = (
        coordinates[SA2_NAME_COLUMN]
        .astype("string")
    )

    coordinates[SA2_CODE_COLUMN] = (
        coordinates[SA2_CODE_COLUMN]
        .astype("string")
    )

    # ---------------------------------------------------------------
    # Find coordinates that still require lookup
    # ---------------------------------------------------------------

    missing = coordinates[
        coordinates[SA2_CODE_COLUMN].isna()
    ].copy()

    print(
        f"Unique coordinates: "
        f"{len(coordinates)}"
    )

    print(
        f"Coordinates already known: "
        f"{len(coordinates) - len(missing)}"
    )

    print(
        f"New coordinates to query: "
        f"{len(missing)}"
    )

    # ---------------------------------------------------------------
    # Query previously unknown coordinates
    # ---------------------------------------------------------------

    if not missing.empty:
        results = []

        total = len(missing)

        for number, row in enumerate(
            missing.itertuples(),
            start=1
        ):
            result = query_sa2(
                (
                    row.latitude,
                    row.longitude,
                    api_key,
                )
            )

            results.append(result)

            if (
                number % 50 == 0
                or number == total
            ):
                print(
                    f"Queried {number}/{total} "
                    f"new coordinates"
                )

        result_df = pd.DataFrame(
            results,
            index=missing.index,
            columns=[
                SA2_NAME_COLUMN,
                SA2_CODE_COLUMN
            ]
        ).astype("string")

        # Store newly obtained results
        coordinates.loc[
            missing.index,
            [
                SA2_NAME_COLUMN,
                SA2_CODE_COLUMN
            ]
        ] = result_df

    # ---------------------------------------------------------------
    # Attach SA2 results to every Airbnb observation
    # ---------------------------------------------------------------

    df = df.merge(
        coordinates,
        on=[
            "latitude",
            "longitude"
        ],
        how="left",
        validate="many_to_one"
    )

    missing_count = (
        df[SA2_CODE_COLUMN]
        .isna()
        .sum()
    )

    print(
        f"Rows with an SA2 match: "
        f"{len(df) - missing_count}"
    )

    print(
        f"Rows without an SA2 match: "
        f"{missing_count}"
    )

    # This return is essential
    return df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """
    Load cleaned Airbnb data, add SA2 information,
    and save the enriched dataset.
    """

    api_key = os.getenv("API_KEY")

    if not api_key:
        print(
            "API_KEY environment variable is not set."
        )
        sys.exit(1)

    # ---------------------------------------------------------------
    # Read cleaned Airbnb dataset
    # ---------------------------------------------------------------

    df = pd.read_csv(
        CLEANED_AIRBNB_FILE
    )

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

    # ---------------------------------------------------------------
    # Test the API
    # ---------------------------------------------------------------

    print("Running test query...")

    test_result = test_single_query(
        df,
        api_key
    )

    if test_result == (None, None):
        print(
            "Warning: test query did not "
            "return an SA2 match."
        )

        print(
            "Check the API key, layer ID, "
            "and coordinate values."
        )

        sys.exit(1)

    print("Test query successful.")
    print("Processing all rows...")

    # ---------------------------------------------------------------
    # Add SA2 columns
    # ---------------------------------------------------------------

    df = add_sa2_data(
        df,
        api_key
    )

    # ---------------------------------------------------------------
    # Convert SA2 code to nullable integer
    # ---------------------------------------------------------------

    df[SA2_CODE_COLUMN] = pd.to_numeric(
        df[SA2_CODE_COLUMN],
        errors="coerce"
    ).astype("Int64")

    # ---------------------------------------------------------------
    # Save completed dataset
    # ---------------------------------------------------------------

    df.to_csv(
        CLEANED_AIRBNB_SA2_FILE,
        index=False
    )

    print(
        f"Saved output to "
        f"{CLEANED_AIRBNB_SA2_FILE}"
    )

    print("No errors")


if __name__ == "__main__":
    main()