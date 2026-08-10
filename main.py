import re

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

# month year column code to be added here


def read_data(data_path="data"):
    """

    name format should be: "listings-yy-mm.csv"

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
        year, month = data_collection_date(name)
        df = pd.read_csv(f"{data_path}/{name}")
        df["month"] = month
        df["year"] = year
        data_files.append(df)

    # combines the list of datasets into one pandas data frame
    return pd.concat(data_files)


def data_collection_date(data_file_name):
    """
    Takes the filename of a data frame and returns a tuple
    containing the year and month the data was collected in
    numerical form.
    (year, month) = add_data_collection_date("listings-25-10.csv")
    (year, month) == (25, 10)
    Filename should have the form: "listings-yy-mm.csv"
    """

    # yy_mm = re.search("\d\d-\d\d", data_file_name)
    # yy_mm = yy_mm.group()
    yy_mm = data_file_name[-9:-4]
    year = int(yy_mm[:2])
    month = int(yy_mm[-2:])
    return year, month


# price histogram

# remove missing price values??


def plot_hist(values, title):
    """plot the prices in a histogram"""
    price = values["price"]
    plt.figure(figsize=(8, 6))
    axes = plt.axes()
    axes.hist(
        price, bins=np.linspace(0, 1500, 16), edgecolor="steelblue", color="skyblue"
    )
    axes.set_title(title)
    axes.set_xlabel("Nightly price ($)")
    axes.set_ylabel("Count")


# days since last review --> chch_data daytime format is in
def str_to_date(data):
    """convert string format of date in last-review column (YYYY-MM-DD) to date"""
    data["last_review"] = pd.to_datetime(
        data["last_review"], format="%Y-%m-%d", errors="coerce"
    )  # change NaN from float


def days_since_review(data):
    """how many days since the last review??"""
    data["days_since_last_review"] = (
        pd.Timestamp.today() - data["last_review"]
    ).dt.days


# plot in histogram
def plot_day_hist(day_values):
    """plot days since last view into a histogram"""
    days = day_values["days_since_last_review"]
    plt.figure(figsize=(8, 6))
    axes = plt.axes()
    axes.hist(days, edgecolor="orchid", color="thistle", bins=np.linspace(0, 3000, 31))
    axes.set_title("Days since last review (CHCH)")
    axes.set_xlabel("Days")
    axes.set_ylabel("Count")


# plot in histogram
def plot_rev_hist(rev_values):
    """plot days since last review into a histogram"""
    reviews = rev_values["number_of_reviews"]
    plt.figure(figsize=(8, 6))
    axes = plt.axes()

    counts, bins, patches = axes.hist(
        reviews,
        edgecolor="seagreen",
        color="mediumaquamarine",
        bins=np.linspace(100, 1000, 21),
    )
    # recolor bins for reviews in top 10%
    for patch, left_edge in zip(patches, bins[:-1]):
        if left_edge >= 183:
            patch.set_facecolor("powderblue")

    # legend time
    legend_elements = [
        Patch(
            facecolor="mediumaquamarine",
            edgecolor="seagreen",
            label="Bottom 90% of reviews (<183)",
        ),
        Patch(
            facecolor="powderblue",
            edgecolor="seagreen",
            label="Top 10% of reviews (>=183)",
        ),
    ]

    axes.set_title("Number of reviews per property in CHCH")
    axes.set_xlabel("Number of Reviews")
    axes.set_ylabel("Count/Number of properties")
    axes.legend(handles=legend_elements, title="Review count")


def main():
    data = read_data()
    data.to_csv("data/concatenated data 25-10 to 26-06.csv")
    print(data[["number_of_reviews", "price"]].head())
    print(data[["number_of_reviews", "price"]].describe())
    print(data["price"].isna().sum())

    # filter data by chch location only (temporary)
    chch_data = data[data["neighbourhood_group"] == "Christchurch City"]

    # days since last review
    str_to_date(chch_data)

    # summary stats to go here

    # plot nz nightly price data
    nz_title = "Price density of AirBnBs in New Zealand"
    plot_hist(data, nz_title)
    # plot chch price data
    chch_title = "Price density of AirBnBs in Christchurch"
    plot_hist(chch_data, chch_title)  # using max price of $1500

    # check str to date conversion worked
    print(chch_data["last_review"].dtype)
    # calculate days since last review
    days_since_review(chch_data)
    # call days since last review hist
    plot_day_hist(chch_data)

    # plot hist of number of reviews for chch
    plot_rev_hist(chch_data)

    chch_90 = np.quantile(chch_data["number_of_reviews"], 0.9)
    nz_90 = np.quantile(data["number_of_reviews"], 0.9)
    print(
        f"The top 10% of properties reviewed in Christchurch are reviewed more than {chch_90:.0f} times"
    )
    print(
        f"The top 10% of properties reviewed nationwide are reviewed more than {nz_90:.0f} times"
    )
    # check how many properties in chch are reviewed 182 times to get difference
    # alex/syamily to generate final visualisation
    # alex check plots and edit axis labels
    plt.show()  # generate plots


if __name__ == "__main__":
    main()
