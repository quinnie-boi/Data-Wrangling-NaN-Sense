from constants import CLEANED_AIRBNB_FILE, CLEANED_BONDS_FILE, UNCLEANED_AIRBNB_FILE, UNCLEANED_BONDS_FILE
import os

# month year column code to be added here


def read_data(data_source="data/raw"):
    """
    name format should be: "listings-yy-mm.csv"
    where yy-mm is the date the data was scraped.

    reads the 9 listings.csv files from the /data/raw folder then
    merges them in to one dataset which is returned.
    Also adds a year and month column for the scrape date.

    data_path: the relative path to where the csv files are stored
    """

    # Automatically finds all files containing "listings" in the name
    pattern = "listings"
    file_names = [f for f in os.listdir(data_source) if pattern in f]

    # reads all of the files using pandas (pd), adding them to a list
    data_files = []
    for name in file_names:
        year, month = data_collection_date(name)
        df = pd.read_csv(f"{data_source}/{name}")
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
    return (pd.to_datetime("2026-06-22",format="%Y-%m-%d") - data["last_review"]).dt.days

def open_airbnb_dataset(path = UNCLEANED_AIRBNB_FILE):
    return pd.read_csv(path,
        parse_dates=["last_review"],
        index_col=0 #use id as the index column
    )

def open_quarterly_dataset(path = UNCLEANED_BONDS_FILE):
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

    # standardise Number Of Beds column <- do not need this if ALL & ALL is the aggrogate data
    # df['Number Of Beds'] = df['Number Of Beds'].replace(to_replace=['5', '6', '7', '8', '9', '15'], value="5+")

    df['Number Of Beds'] = df['Number Of Beds'].astype('category')
    df['Dwelling Type'] = df['Dwelling Type'].astype('category')
    df.rename(columns={'Location Id': 'sa2_code'}, inplace=True)

    df = df[
        (df["Dwelling Type"] == "ALL") &
        (df["Number Of Beds"] == "ALL")
        ].copy()

    return df

def clean_both_datasets():
    """
    Clean both datasets and restrict them to a common date range.
    """
    rental_bonds_data = clean_quarterly_dataset()
    airbnb_data = cleaned_airbnb_dataset()

    # Ensure date columns are datetime
    rental_bonds_data["TimeFrame"] = pd.to_datetime(
        rental_bonds_data["TimeFrame"]
    )
    airbnb_data["last_review"] = pd.to_datetime(
        airbnb_data["last_review"]
    )

    # Determine latest date available in both datasets
    newest = min(
        rental_bonds_data["TimeFrame"].max(),
        airbnb_data["last_review"].max()
    )

    # Airbnb listing data is only valid from October 2025 onwards
    oldest = pd.to_datetime("2025-10-01")

    # Filter Airbnb data
    airbnb_data = airbnb_data[
        airbnb_data["last_review"].between(oldest, newest)
    ].copy()

    # Filter rental bond data
    rental_bonds_data = rental_bonds_data[
        rental_bonds_data["TimeFrame"].between(oldest, newest)
    ].copy()

    print(f"Data combined from {oldest.date()} to {newest.date()}")

    # remove 'ALL' from `Dwelling Type` and `Number of Beds`


    # Save the main cleaned datasets
    rental_bonds_data.to_csv(CLEANED_BONDS_FILE, index=False)
    airbnb_data.to_csv(CLEANED_AIRBNB_FILE, index=False)

    # Create a copy of the cleaned rental data
    cleaned_rentals = rental_bonds_data.copy()

    # Make sure the out folder exists
    os.makedirs("../out", exist_ok=True)

    # Write the copy to out folder
    cleaned_rentals.to_csv(
        "out/cleaned_rentals.csv",
        index=False
    )

    # Also save a copy to Downloads
    output_file = Path.home() / "Downloads" / "cleaned_rentals.csv"
    cleaned_rentals.to_csv(output_file, index=False)

    print(f"Cleaned data saved to: {output_file}")
    print(
        f"Successfully saved the cleaned Airbnb dataset to "
        f"{CLEANED_AIRBNB_FILE}"
    )
    print(
        f"Successfully saved the cleaned rental bonds dataset to "
        f"{CLEANED_BONDS_FILE}"
    )

    return cleaned_rentals, airbnb_data



def main():
    clean_both_datasets()

if __name__ == "__main__":
    main()
