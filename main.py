import numpy as np
import pandas as pd


def read_data(data_path="data"):
    """
    reads the 9 listings.csv files from the /data folder then
    merges them in to one dataset which is returned.

    data_path: the relative path to where the csv files are stored
    """
    import os

    # Automatically finds all files containing "listings" in the name
    pattern = "listings"
    file_names = [f for f in os.listdir(data_path) if pattern in f]

    # reads all of the files using pandas (pd), adding them to a list
    data_files = []
    for name in file_names:
        data_files.append(pd.read_csv(f"{data_path}/{name}"))

    # combines the list of datasets into one pandas data frame
    return pd.concat(data_files)


def main():
    data = read_data()
    print(data[["number_of_reviews", "price"]].head())
    print(data[["number_of_reviews", "price"]].describe())
    print(data["price"].isna().sum())


if __name__ == "__main__":
    main()
