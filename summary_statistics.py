"""
Created for Deliverable 3

Creates summary statistics for the airbnb data for both New Zealand and
Christchurch. Produces four figures and prints information to console.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from clean_datasets import cleaned_airbnb_dataset, open_airbnb_dataset

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
        pd.to_datetime("2026-06-22",format="%Y-%m-%d") - data["last_review"]
    ).dt.days

# plot in histogram
def plot_day_hist(day_values):
    """plot days since last view into a histogram"""
    days = day_values["days_since_last_review"]
    plt.figure(figsize=(8, 6))
    axes = plt.axes()
    axes.hist(days, edgecolor="orchid", color="thistle", bins=np.linspace(0, 3000, 31))
    axes.set_title("Days since last review (CHCH, 19 June 2026)")
    axes.set_xlabel("Days")
    axes.set_ylabel("Count")

# plot in histogram
def plot_rev_hist(rev_values):
    """number of reviews per property in CHCH"""
    reviews = rev_values["number_of_reviews"]
    plt.figure(figsize=(8, 6))
    axes = plt.axes()

    bins = np.concatenate([
        np.linspace(0, 600, 30),
        [np.inf],
    ])
    counts, bins, patches = axes.hist(
        reviews,
        edgecolor="seagreen",
        color="mediumaquamarine",
        bins=bins,
    )
    # recolor bins for reviews in top 10%
    for patch, left_edge in zip(patches, bins[:-1]):
        if left_edge >= 183:
            patch.set_facecolor("powderblue")
    # recolor top end
    patches[-1].set_facecolor('coral')
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
            label="Top 10% of reviews (>=183 and <600)",
        ),
        Patch(
            facecolor="coral",
            edgecolor="seagreen",
            label='>600 reviews'
        )
    ]

    axes.set_title("Number of reviews per property in CHCH")
    axes.set_xlabel("Number of Reviews")
    axes.set_ylabel("Count/Number of properties")
    axes.legend(handles=legend_elements, title="Review count")

def main():
    data = open_airbnb_dataset()
    chch_data = cleaned_airbnb_dataset()    # summary stats to go here

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


if __name__ == '__main__':
    main()
