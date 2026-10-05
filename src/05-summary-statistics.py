"""
Created for Deliverable 3

Creates summary statistics for the airbnb data for both New Zealand and
Christchurch. Produces four figures and prints information to console.
"""
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from constants import UNCLEANED_AIRBNB_FILE, CLEANED_AIRBNB_FILE, OUT_DIR

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
    axes.set_title("Days since last review in Christchurch")
    axes.set_xlabel("Days")
    axes.set_ylabel("Count")

# plot in histogram
def plot_rev_hist(rev_values):
    """number of reviews per property in CHCH"""
    reviews = rev_values["number_of_reviews"].dropna()
    plt.figure(figsize=(8, 6))
    axes = plt.axes()

    max_reviews = rev_values["number_of_reviews"].max()
    bins = np.concatenate([
        np.linspace(0, 600, 30),
        [max_reviews + 1],
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
    # Make sure output directory exists
    OUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Read combined New Zealand Airbnb data
    data = pd.read_csv(
        UNCLEANED_AIRBNB_FILE,
        parse_dates=["last_review"]
    )

    # Read cleaned Christchurch Airbnb data
    chch_data = pd.read_csv(
        CLEANED_AIRBNB_FILE,
        parse_dates=["last_review"]
    )

    # Plot NZ nightly price data
    nz_title = "Price density of AirBnBs in New Zealand"

    plot_hist(
        data,
        nz_title
    )

    plt.savefig(
        OUT_DIR / "nz_airbnb_price.png",
        bbox_inches="tight"
    )

    plt.close()

    # Plot Christchurch price data
    chch_title = "Price density of AirBnBs in Christchurch"

    plot_hist(
        chch_data,
        chch_title
    )

    plt.savefig(
        OUT_DIR / "chch_airbnb_price.png",
        bbox_inches="tight"
    )

    plt.close()

    print(
        "Christchurch last_review dtype:",
        chch_data["last_review"].dtype
    )

    # Plot days since last review
    plot_day_hist(chch_data)

    plt.savefig(
        OUT_DIR / "chch_days_since_review.png",
        bbox_inches="tight"
    )

    plt.close()

    # Plot number of reviews
    plot_rev_hist(chch_data)

    plt.savefig(
        OUT_DIR / "chch_number_of_reviews.png",
        bbox_inches="tight"
    )

    plt.close()

    # Calculate review percentiles
    chch_90 = np.quantile(
        chch_data["number_of_reviews"],
        0.9
    )

    nz_90 = np.quantile(
        data["number_of_reviews"],
        0.9
    )

    print(
        f"The top 10% of properties reviewed in Christchurch "
        f"are reviewed more than {chch_90:.0f} times"
    )

    print(
        f"The top 10% of properties reviewed nationwide "
        f"are reviewed more than {nz_90:.0f} times"
    )

    print(f"Plots successfully saved to {OUT_DIR}")


if __name__ == "__main__":
    main()

