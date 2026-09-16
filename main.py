import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

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



def open_listings_dataset(path = "data/listings_25-10_26-06.csv"):
    return pd.read_csv(path,
        parse_dates=["last_review"],
        index_col=0 # use id as the index column
    )

def open_quarterly_dataset(path = "data/quarterly_2025_2026.csv"):
    return pd.read_csv(path,
        parse_dates=["TimeFrame"]
    )

def clean_quarterly_dataset():
    """
    Clean and structure as much of the Rental Bond dataset
    as possible. More is done in-tandem with the AirBnB datasets.
    """
    # filter quart-tenancy/bond data to same dates as airbnb
    df = open_quarterly_dataset()

    # Remove the 803 weird and unsuable rows containg 4-5 NA Values
    df.dropna(
        subset = ["Median Rent"],
        inplace=True
    )

    # Remove rows where Location Id == -99
    df = df[df["Location Id"] != -99]

    # standardise Number Of Beds column
    df['Number Of Beds'] = df['Number Of Beds'].replace(to_replace=['5', '6', '7', '8', '9', '15'], value="5+")

    df['Number Of Beds'] = df['Number Of Beds'].astype('category')
    df['Dwelling Type'] = df['Dwelling Type'].astype('category')

    return df

def clean_airbnb_dataset():
    """"""
    df = open_listings_dataset()
    df = df[df["neighbourhood_group"] == "Christchurch City"].copy()

    # drop select columns from airbnb dataset
    df.drop(axis=1, labels=[
        "name",
        "host_name",
        "neighbourhood_group", # they are all in Christchurch City
        "minimum_nights",
        "reviews_per_month",
        "license"
    ], inplace=True)

    # Adds a new column in-place
    # TODO Change the API of this function
    days_since_review(df)

    # Coerce columns into category datatype,
    # automatically generated based on existing values.
    for category in ['neighbourhood', 'room_type']:
        df[category] = df[category].astype('category')

    return df

def main():
    rental_data = clean_quarterly_dataset()
    airbnb_data = clean_airbnb_dataset()

    # TODO The oldest date is 2020-01-01 which is IMPOSSIBLE given
    # the listings data only goes back to 25-10.
    oldest = max(rental_data["TimeFrame"].min(), airbnb_data["last_review"].min())
    newest = min(rental_data["TimeFrame"].max(), airbnb_data["last_review"].max())

    # quarterly: 2020-01-01 to 2026-04-01
    # listings: 2013-03-03 to 2026-06-22

    # Remove rows that are not within the range
    airbnb_data = airbnb_data[airbnb_data["last_review"].ge(oldest)]
    airbnb_data = airbnb_data[airbnb_data["last_review"].le(newest)]
    # doesn't actually change anything atm
    rental_data = rental_data[rental_data["TimeFrame"].ge(oldest)]
    rental_data = rental_data[rental_data["TimeFrame"].le(newest)]

    print(oldest, newest)

    # Print a pivot table containing the
    # frequency of each category
    print(rental_data['Number Of Beds'].value_counts())

    # Check that the categories are correct
    # print(quarterly_data['Number Of Beds'].cat.categories.tolist())
    # print(quarterly_data['Dwelling Type'].cat.categories.tolist())

    # Check that the datatypes of each column are correct
    # print(airbnb_data.dtypes)
    # print(rental_data.dtypes)

    # print(rental_data.describe())
    # print(rental_data.isna().sum())

if __name__ == "__main__":
    main()
