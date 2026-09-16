import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch


def read_data(data_source="data/raw"):
    """
    name format should be: "listings-yy-mm.csv"
    where yy-mm is the date the data was scraped.

    reads the 9 listings.csv files from the /data/raw folder then
    merges them in to one dataset which is returned.
    Also adds a year and month column for the scrape date.

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
        df["scrape_month"] = month
        df["scrape_year"] = year
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

# days since last review --> chch_data daytime format is in
def str_to_date(data):
    """convert string format of date in last-review column (YYYY-MM-DD) to date"""
    data["last_review"] = pd.to_datetime(
        data["last_review"], format="%Y-%m-%d", errors="coerce"
    )  # change NaN from float

def days_since_review(data):
    """
    Add a column containing the number of days since last review, relative to the
    latest date in the data. i.e. data["days_since_last_review"].min() == 0
    """
    latest_review = data["last_review"].max()
    print("INFO <days_since_review>: latest review was", latest_review)

    data["days_since_last_review"] = (
        pd.to_datetime(latest_review,format="%Y-%m-%d") - data["last_review"]
    ).dt.days

def deliverable_3(data):
    print(data[["number_of_reviews", "price"]].head())
    print(data[["number_of_reviews", "price"]].describe())

    # filter data by chch location only (temporary)
    chch_data = data[data["neighbourhood_group"] == "Christchurch City"]
    print(chch_data["price"].isna().sum())
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

def merge_and_save_listings(source_directory = "data/raw", outpath = "data/listings_25-10_26-06.csv"):
    data = read_data(source_directory)
    data.to_csv(outpath)

def open_listings_dataset(path = "data/listings_25-10_26-06.csv"):
    return pd.read_csv(path,
        parse_dates=["last_review"]
    )

def open_quarterly_dataset(path = "data/quarterly_2025_2026.csv"):
    return pd.read_csv(path,
        parse_dates=["TimeFrame"]
    )


def main():
    data = open_listings_dataset()
    # deliverable 4

    print(data[["number_of_reviews", "price"]].head())
    print(data[["number_of_reviews", "price"]].describe())
    chch_data = data[data["neighbourhood_group"] == "Christchurch City"].copy()
    # drop select columns from airbnb dataset
    chch_data.drop(axis=1, labels=[
        "Unnamed: 0", # remove the automatic 0 indexed row number.
        "name",
        "host_name",
        "neighbourhood_group", # they are all in Christchurch City
        "minimum_nights",
        "reviews_per_month",
        "license"
    ], inplace=True)

    days_since_review(chch_data)

    # filter quart-tenancy/bond data to same dates as airbnb
    quarterly_data = open_quarterly_dataset()

    print(quarterly_data.columns)
    # Remove the 803 weird and unsuable rows containg 4-5 NA Values
    quarterly_data.dropna(
        subset = ["Median Rent"],
        inplace=True
    )

    # Remove rows where Location Id == -99
    quarterly_data = quarterly_data[quarterly_data["Location Id"] != -99]

    # standardise Number Of Beds column
    quarterly_data['Number Of Beds'] = quarterly_data['Number Of Beds'].replace(to_replace=['5', '6', '7', '8', '9', '15'], value="5+")
    print(quarterly_data['Number Of Beds'].value_counts())
    print(quarterly_data.dtypes)


    # drop select columns from bond dataset
    oldest = max(quarterly_data["TimeFrame"].min(), data["last_review"].min())
    newest = min(quarterly_data["TimeFrame"].max(), data["last_review"].max())
    # oldest, newest = quarterly_data["TimeFrame"].min(), data["last_review"].max()
    # print(type(oldest), type(newest))
    # quarterly: 2020-01-01 to 2026-04-01
    # listings: 2013-03-03 to 2026-06-22
    print(data[data["last_review"] == data["last_review"].min()][["last_review", "host_id", "year"]].describe())

    data = data[data["last_review"].ge(oldest)]
    data = data[data["last_review"].le(newest)]
    # doesn't actually change anything atm
    quarterly_data = quarterly_data[quarterly_data["TimeFrame"].ge(oldest)]
    quarterly_data = quarterly_data[quarterly_data["TimeFrame"].le(newest)]

    # quarterly_data.drop(axis=1, labels=[
    #     "Total Bonds",
    #     "Active Bonds",
    #     "Closed Bonds"
    # ], inplace=True)

    # print(quarterly_data.describe())
    # print(quarterly_data.isna().sum())


if __name__ == "__main__":
    main()
