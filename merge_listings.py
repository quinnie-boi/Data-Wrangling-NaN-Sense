"""
Created for Deliverable 3

Imports the nine airbnb listing dataset csv files from a folder and
merges them into one larger dataset which is saved to disk.
"""

from constants import *
import os
import pandas as pd


def file_names_in(source_dir, pattern = "listings"):
    """
    Returns a list of file names in `source_dir` folder
    that contain `pattern` in the name
    """
    return [f for f in os.listdir(source_dir) if pattern in f]

def data_collection_date(data_file_name):
    """ Helper Function
    Takes the filename of a data frame and returns a tuple
    containing the year and month the data was collected in
    numerical form. Filename should have the form
    "listings-yy-mm.csv"
    Usage:
    > add_data_collection_date("listings-25-10.csv")
    > (25, 10)
    """
    # yy_mm = re.search("\d\d-\d\d", data_file_name)
    # yy_mm = yy_mm.group()
    try:
        # strip the prefix and suffix
        yy_mm = data_file_name.strip("listings-.csv")
        year = int(yy_mm[:2])
        month = int(yy_mm[-2:])
        return year, month
    except ValueError:
        raise Exception(f"Couldn't extract date info from the following file: {data_file_name}.\
            \nread_data() tries to merge ALL files in the given directory. Make sure only the\
            nine listing files are in the data_source directory and ensure they following the\
            correct naming scheme defined in the README and read_data.")

def read_data(source_dir=UNCLEANED_AIRBNB_DIR):
    """
    name format should be: "listings-yy-mm.csv"
    where yy-mm is the date the data was scraped.

    reads the 9 listings.csv files from the /data/raw folder then
    merges them in to one dataset which is returned.
    Also adds a year and month column for the scrape date.

    data_path: the relative path to where the csv files are stored
    """

    # reads all of the files using pandas (pd), adding them to a list
    data_files = []
    for name in file_names_in(source_dir):
        year, month = data_collection_date(name)
        # keep track of dates as yy-mm
        df = pd.read_csv(f"{source_dir}/{name}")
        df["scrape_month"] = month
        df["scrape_year"] = year
        data_files.append(df)

    merged_data = pd.concat(data_files)
    # combines the list of datasets into one pandas data frame
    return merged_data

def main():
    data = read_data()
    data.to_csv(UNCLEANED_AIRBNB_FILE)
    print(f"Successfully saved the merged csvs to {UNCLEANED_AIRBNB_FILE}")

if __name__ == "__main__":
    main()
