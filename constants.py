# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
"""
Constants for the other python files to use, so names are consistent and easy to update.
"""
import os

DATA_DIR = "data"
UNCLEANED_AIRBNB_DIR = os.path.join(DATA_DIR, "uncleaned_airbnb_listings")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")


UNCLEANED_AIRBNB_FILE = os.path.join(DATA_DIR, "uncleaned_airbnb_listings.csv")
UNCLEANED_BONDS_FILE = os.path.join(DATA_DIR, "uncleaned_bonds.csv")

AIRBNB_FILE_NAME = "chch_airbnb.csv"
BONDS_FILE_NAME = "tenancy_bonds.csv"
MERGED_FILE_NAME = "airbnb_rental_sa2.csv"
CLEANED_AIRBNB_FILE = os.path.join(CLEANED_DIR, AIRBNB_FILE_NAME)
CLEANED_BONDS_FILE = os.path.join(CLEANED_DIR, BONDS_FILE_NAME)
CLEANED_MERGED_DATASET_FILE = os.path.join(CLEANED_DIR, MERGED_FILE_NAME)

EXPECTED_AIRBNB_FILE_COUNT = 9
AIRBNB_FILE_PREFIX = "listings-"
AIRBNB_FILE_SUFFIX = ".csv"
