from constants import CLEANED_AIRBNB_FILE, CLEANED_BONDS_FILE, UNCLEANED_AIRBNB_FILE, UNCLEANED_BONDS_FILE
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_hist(values, title):
    """plot the prices in a histogram"""
    values = pd.read_csv(CLEANED_AIRBNB_FILE)
    price = values["price"]
    plt.figure(figsize=(8, 6))
    axes = plt.axes()
    axes.hist(
        price, bins=np.linspace(0, 1500, 16), edgecolor="steelblue", color="skyblue"
    )
    axes.set_title(title)
    axes.set_xlabel("Nightly price ($)")
    axes.set_ylabel("Count")
    plt.show()

def main():
    plot_hist(CLEANED_AIRBNB_FILE,"Price distribution of Airbnbs in Chirstchurch")

if __name__ == "__main__":
    main()