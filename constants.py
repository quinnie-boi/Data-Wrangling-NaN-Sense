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

AIRBNB_FILE_NAME = "chch_airbnb_listings.csv"
BONDS_FILE_NAME = "tenancy_bonds.csv"
MERGED_FILE_NAME = "merged_listings_and_bonds.csv"
CLEANED_AIRBNB_FILE = os.path.join(CLEANED_DIR, AIRBNB_FILE_NAME)
CLEANED_BONDS_FILE = os.path.join(CLEANED_DIR, BONDS_FILE_NAME)
CLEANED_MERGED_DATASET_FILE = os.path.join(CLEANED_DIR, MERGED_FILE_NAME)

EXPECTED_AIRBNB_FILE_COUNT = 9
AIRBNB_FILE_PREFIX = "listings-"
AIRBNB_FILE_SUFFIX = ".csv"

EXPECTED_ROOT_FILES = [
    'constants.py',
    'setup_project.py',
    'summary_statistics_2.py',
    'merge_listings_3.py',
    'clean_datasets_4.py',
    'main_5.py',
    'add_sa2_codes_v5a.py',
    'add_sa2_codes_v5b.py',
    'README.md',
    'using_git.md',
    '.gitignore',
    '.git',
    'data',
    'code-of-conduct.md',
    '.idea'
]
