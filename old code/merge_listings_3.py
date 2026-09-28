"""
Created for Deliverable 3

Imports the nine airbnb listing dataset csv files from a folder and
merges them into one larger dataset which is saved to disk.
"""

from constants import *
import os
import pandas as pd


def file_names_in(source_dir, pattern="listings"):
    """
    Returns a list of file names in `source_dir` folder
    that contain `pattern` in the name.
    """
    return [f for f in os.listdir(source_dir) if pattern in f]


def data_collection_date(data_file_name):
    """
    Takes a filename such as "listings-25-10.csv"
    and returns (25, 10).
    """
    try:
        yy_mm = (
            data_file_name
            .removeprefix("listings-")
            .removesuffix(".csv")
        )

        year = int(yy_mm[:2])
        month = int(yy_mm[-2:])

        return year, month

    except ValueError:
        raise Exception(
            f"Couldn't extract date info from the following file: "
            f"{data_file_name}."
        )


def read_data(source_dir=UNCLEANED_AIRBNB_DIR):
    """
    Name format should be: "listings-yy-mm.csv"
    where yy-mm is the date the data was scraped.

    Reads each listings CSV file, adds scrape date information
    to that individual dataset, then merges all datasets.

    Adds scrape_year, scrape_month, and quarter columns.

    source_dir: the path to where the CSV files are stored
    """

    data_files = []

    # Get listing filenames
    file_names = file_names_in(source_dir)

    for filename in file_names:

        # Get scrape year and month FIRST
        scrape_year, scrape_month = data_collection_date(filename)

        # Calculate quarter from scrape month
        scrape_quarter = (scrape_month - 1) // 3 + 1

        # Read this individual CSV
        file_path = os.path.join(source_dir, filename)
        df = pd.read_csv(file_path)

        # Modify this individual dataset BEFORE merging
        df["scrape_year"] = scrape_year
        df["scrape_month"] = scrape_month
        df["quarter"] = scrape_quarter

        # Add completed individual dataset to list
        data_files.append(df)

    # Merge only after ALL individual files have been modified
    merged_data = pd.concat(data_files, ignore_index=True)

    return merged_data


def main():
    data = read_data()

    data.to_csv(UNCLEANED_AIRBNB_FILE, index=False)

    print(
        f"Successfully saved the merged csvs to "
        f"{UNCLEANED_AIRBNB_FILE}"
    )

if __name__ == "__main__":
    main()
