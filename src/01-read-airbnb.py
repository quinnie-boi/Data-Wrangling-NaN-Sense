import os
import pandas as pd
from constants import (
UNCLEANED_AIRBNB_DIR,
AIRBNB_FILE_PREFIX,
AIRBNB_FILE_SUFFIX,
UNCLEANED_AIRBNB_FILE
)


def file_names_in(source_dir=UNCLEANED_AIRBNB_DIR):
    """
    Returns a sorted list of Airbnb CSV filenames in source_dir
    that match the configured prefix and suffix.
    """
    return sorted(
    f for f in os.listdir(source_dir)
    if f.startswith(AIRBNB_FILE_PREFIX)
    and f.endswith(AIRBNB_FILE_SUFFIX)
    )


def data_collection_date(data_file_name):
    """
    Takes a filename such as "listings-25-10.csv"
    and returns (25, 10).
    """
    try:
        yy_mm = (
            data_file_name
            .removeprefix(AIRBNB_FILE_PREFIX)
            .removesuffix(AIRBNB_FILE_SUFFIX)
        )

        year, month = map(int, yy_mm.split("-"))
        if not 1 <= month <= 12:
            raise ValueError
        return year, month

    except ValueError:
        raise ValueError(
            f"Couldn't extract date info from the following file: "
            f"{data_file_name}."
    )


def read_data(source_dir=UNCLEANED_AIRBNB_DIR):
    """
    Reads Airbnb listing CSV files from source_dir.

    Filename format should be:
        listings-yy-mm.csv

    Adds scrape_year, scrape_month, and quarter columns
    to each dataset before combining them. Also creates a combined Year and Quarter column.

    source_dir: path to the directory containing the CSV files.
    """

    data_files = []

    # Get listing filenames
    file_names = file_names_in(source_dir)

    if not file_names:
        raise FileNotFoundError(
            f"No Airbnb listing files found in {source_dir}"
        )

    for filename in file_names:

        # Get scrape year and month from filename
        scrape_year, scrape_month = data_collection_date(filename)

        # Calculate quarter from scrape month
        scrape_quarter = (scrape_month - 1) // 3 + 1

        # Read individual CSV
        file_path = os.path.join(source_dir, filename)
        df = pd.read_csv(file_path)

        # Add scrape date information
        df["scrape_year"] = scrape_year
        df["scrape_month"] = scrape_month
        df["quarter"] = scrape_quarter
        df["year_quarter"] = f"{scrape_year:02d}Q{scrape_quarter}"

        # Add completed dataset to list
        data_files.append(df)

    # Combine all listing datasets
    merged_data = pd.concat(data_files, ignore_index=True)
    return merged_data


def main():
    uncleaned_airbnb_listings = read_data()
    os.makedirs(
        os.path.dirname(UNCLEANED_AIRBNB_FILE),
        exist_ok=True
    )
    uncleaned_airbnb_listings.to_csv(
        UNCLEANED_AIRBNB_FILE,
        index=False
    )
    print("Airbnb listings successfully merged.")
if __name__ == "__main__":
    main()
