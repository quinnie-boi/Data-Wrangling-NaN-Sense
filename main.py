import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# price histogram

# remove missing price values??

def plot_hist(values, title):
    """plot the prices in a histogram"""
    price = values['price']
    plt.figure(figsize=(8, 6))
    axes = plt.axes()
    axes.hist(price, bins=np.linspace(0,1500,16), edgecolor='steelblue', color='skyblue')
    axes.set_title(title)
    axes.set_xlabel('Nightly price ($)')
    axes.set_ylabel('Count')



def main():
    data = read_data()
    print(data[["number_of_reviews", "price"]].head())
    print(data[["number_of_reviews", "price"]].describe())
    print(data["price"].isna().sum())
    # filter data by chch location only
    chch_data = data[data['neighbourhood_group'] == 'Christchurch City']
    # plot nz
    nz_title = "Price density of AirBnBs in New Zealand"
    plot_hist(data, nz_title)
    # plot chch price titles
    chch_title = "Price density of AirBnBs in Christchurch"
    plot_hist(chch_data, chch_title)  # using max price of $1500
    plt.show()

if __name__ == "__main__":
    main()
