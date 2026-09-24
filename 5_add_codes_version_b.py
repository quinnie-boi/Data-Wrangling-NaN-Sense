"""
Deliverable 5

Section where you need to query the Koordinates API.

Add SA22019 area codes to a dataset containing latitude and longitude
columns using the Stats NZ Vector Query API.

Usage:
    python add_sa2_codes.py API_KEY

Example:
    python add_sa2_codes.py cleaned_airbnb.csv abc123xyz
"""


######### lolololol
from calendar import month_name

from numpy._core import float64

from constants import CLEANED_AIRBNB_FILE
import json
import multiprocessing as mp
import sys
import urllib.parse
import urllib.request

import pandas as pd

LAYER_ID = 98970
OUTPUT_COLUMN = "SA22019"

# Query settings
QUERY_MAX_RESULTS = 1
QUERY_RADIUS_METRES = 500
QUERY_GEOMETRY = "false"
QUERY_WITH_FIELD_NAMES = "true"


# def query_sa2_code(args):
#     """
#     Query the Stats NZ API for a latitude and longitude pair.

#     Returns the matching SA22019_V1_00 value if the returned
#     feature contains the queried point (distance == 0).
#     """

#     latitude, longitude, api_key = args

#     url = (
#         "https://datafinder.stats.govt.nz/services/query/v1/vector.json?"
#         + urllib.parse.urlencode(
#             {
#                 "key": api_key,
#                 "layer": LAYER_ID,
#                 "x": longitude,
#                 "y": latitude,
#                 "max_results": QUERY_MAX_RESULTS,
#                 "radius": QUERY_RADIUS_METRES,
#                 "geometry": QUERY_GEOMETRY,
#                 "with_field_names": QUERY_WITH_FIELD_NAMES,
#             }
#         )
#     )

#     try:
#         with urllib.request.urlopen(url, timeout=30) as response:
#             data = json.loads(response.read().decode("utf-8"))

#         features = (
#             data.get("vectorQuery", {})
#             .get("layers", {})
#             .get(str(LAYER_ID), {})
#             .get("features", [])
#         )

#         if not features:
#             return None

#         feature = features[0]

#         if feature.get("distance", -1) > 0:
#             return None

#         properties = feature.get("properties", {})

#         return properties.get("SA22019_V1_00")

#     except Exception as exc:
#         print(
#             f"Failed query for ({latitude}, {longitude}): {exc}"
#         )
#         return None


# def test_single_query(df, api_key):
#     """
#     Run a single query to confirm that the API response
#     structure is correct before processing all rows.
#     """

#     row = df.iloc[0]

#     result = query_sa2_code(
#         (
#             row["latitude"],
#             row["longitude"],
#             api_key,
#         )
#     )

#     print("Test query result:")
#     print(result)

#     return result


# def add_sa2_codes(df, api_key):
#     """
#     Query SA2 codes for all rows in the dataframe.
#     """

#     tasks = [
#         (
#             row.latitude,
#             row.longitude,
#             api_key,
#         )
#         for row in df.itertuples(index=False)
#     ]

#     worker_count = max(1, mp.cpu_count() - 1)

#     with mp.Pool(worker_count) as pool:
#         results = pool.map(query_sa2_code, tasks)

#     df[OUTPUT_COLUMN] = results

#     missing_count = df[OUTPUT_COLUMN].isna().sum()

#     print(f"Rows without an SA2 match: {missing_count}")
#     print(f"Rows with an SA2 match: {len(df) - missing_count}")

#     return df


def test_query(latitude, longitude, api_key):
    """
    Run a single query and print the response details.

    This is useful when checking that the API key,
    coordinates, and response structure are correct.
    """

    url = (
        "https://datafinder.stats.govt.nz/services/query/v1/vector.json?"
        + urllib.parse.urlencode(
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
    )

    print(f"Querying: ({latitude}, {longitude})")
    print(f"URL: {url}")

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        features = (
            data.get("vectorQuery", {})
            .get("layers", {})
            .get(str(LAYER_ID), {})
            .get("features", [])
        )

        if not features:
            print("No matching features found.")
            return None

        feature = features[0]

        print(f"Distance: {feature.get('distance')}")

        properties = feature.get("properties", {})

        sa2_name = properties.get("SA22019_V1_NAME")
        sa2_code = properties.get("SA22019_V1_00")

        print(f"\nSA2 Name: {sa2_name}")
        print(f"SA2 Code: {sa2_code}")

        return sa2_name, sa2_code

    except Exception as exc:
        print(f"Query failed: {exc}")
        return None


SA2_CODE_COLUMN = "sa2_code"
SA2_NAME_COLUMN = "sa2_name"


def query_sa2(args):
    """
    Query the Stats NZ API for a latitude and longitude pair.

    Returns:
        (sa2_name, sa2_code)

    if the queried point falls within the returned polygon
    (distance == 0), otherwise returns (None, None).
    """

    latitude, longitude, api_key = args

    url = (
        "https://datafinder.stats.govt.nz/services/query/v1/vector.json?"
        + urllib.parse.urlencode(
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
    )

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        features = (
            data.get("vectorQuery", {})
            .get("layers", {})
            .get(str(LAYER_ID), {})
            .get("features", [])
        )

        if not features:
            return (None, None)

        feature = features[0]

        if feature.get("distance", -1) > 0:
            return (None, None)

        properties = feature.get("properties", {})

        return (
            properties.get("SA22019_V1_00_NAME"),
            properties.get("SA22019_V1_00"),
        )

    except Exception as exc:
        print(f"Failed query for ({latitude}, {longitude}): {exc}")
        return (None, None)

def test_single_query(df, api_key):
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

def add_sa2_data(df, api_key):
    """
    Query SA2 names and codes for all rows.
    """

    tasks = [
        (
            row.latitude,
            row.longitude,
            api_key,
        )
        for row in df.itertuples(index=False)
    ]

    worker_count = max(1, mp.cpu_count() - 1)

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
    """
    Load the dataset, obtain SA2 codes, and save the result.
    """


    if len(sys.argv) != 2:
        print(
            "Usage: python add_sa2_codes.py API_KEY"
        )
        sys.exit(1)

    api_key = sys.argv[1]

    df = pd.read_csv(CLEANED_AIRBNB_FILE)

    required_columns = {"latitude", "longitude"}

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    print("Running test query...")

    test_result = test_single_query(df, api_key)

    if test_result == (None, None):
        print("Warning: test query did not return an SA2 match.")
        print("Check the API key, layer ID, and coordinate values.")
        sys.exit(1)

    print("Processing all rows...")

    df = add_sa2_data(df, api_key)
    df['sa2_code'] = df['sa2_code'].astype(float64)

    output_csv = CLEANED_AIRBNB_FILE.replace(
        ".csv",
        "_with_sa2.csv",
    )

    df.to_csv(output_csv, index=False)

    print(f"Saved output to {output_csv}")

def test_first_500_rows(df, api_key):
    """
    Run the SA2 lookup on the first 500 rows only.

    Useful for testing performance and API behaviour before
    processing the full dataset.
    """

    test_df = df.head(500).copy()

    print(f"Testing on {len(test_df)} rows...")

    test_df = add_sa2_data(test_df, api_key)

    missing_code_count = test_df[SA2_CODE_COLUMN].isna().sum()
    missing_name_count = test_df[SA2_NAME_COLUMN].isna().sum()
    missing = max(missing_code_count, missing_name_count)

    print("\nTest completed.")
    print(f"Rows processed: {len(test_df)}")
    print(f"Rows matched: {len(test_df) - missing}")
    print(f"Rows missing: {missing}")
    if missing_code_count!=missing_name_count:
        print(f"#Missing names: {missing}")
        print(f"#Missing codes: {missing}")

    print("\nSample results:")
    print(
        test_df[
            [
                "latitude",
                "longitude",
                "sa2_name",
                "sa2_code",
            ]
        ].head()
    )

    return test_df


if __name__ == "__main__":
    main()
    # Test code on 500 rows
    # api_key = sys.argv[1]
    # airbnb = pd.read_csv(CLEANED_AIRBNB_FILE)

    # test_first_500_rows(airbnb, api_key).to_csv("data/no_way.csv")

    # Test code for one query
    # test_query(
    #     latitude=-43.5321,
    #     longitude=172.6362,
    #     api_key=api_key
    # )
