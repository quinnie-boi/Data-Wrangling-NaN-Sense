# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
"""
Constants for the other Python files to use, so names are
consistent and easy to update.
"""

from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Load configuration
# ---------------------------------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

CONFIG_FILE = PROJECT_DIR / "config.yaml"

with CONFIG_FILE.open("r") as file:
    config = yaml.safe_load(file)


# ---------------------------------------------------------------------------
# Directories
# ---------------------------------------------------------------------------

DATA_DIR = PROJECT_DIR / config["data"]["data_dir"]

UNCLEANED_AIRBNB_DIR = (
    DATA_DIR / config["data"]["uncleaned_airbnb_dir"]
)

OUT_DIR = PROJECT_DIR / config["data"]["out_dir"]


# ---------------------------------------------------------------------------
# File names
# ---------------------------------------------------------------------------

CLEANED_AIRBNB_FILE_NAME = config["files"]["airbnb_file_name"]

BONDS_FILE_NAME = config["files"]["bonds_file_name"]

MERGED_FILE_NAME = config["files"]["merged_file_name"]

AIRBNB_SA2_FILE_NAME = config["files"]["airbnb_sa2_file_name"]


# ---------------------------------------------------------------------------
# Raw input files
# ---------------------------------------------------------------------------

RAW_BONDS_FILE = (
    DATA_DIR / config["files"]["bonds_raw_file"]
)

SA2_2019_FILE = (
    DATA_DIR / config["files"]["sa2_2019_file"]
)

JODI_SA2 = (
    DATA_DIR / config["files"]["jodi_sa2"]
)


# ---------------------------------------------------------------------------
# Intermediate output files
# ---------------------------------------------------------------------------

UNCLEANED_AIRBNB_FILE = (
    OUT_DIR / config["files"]["uncleaned_airbnb_file"]
)


# ---------------------------------------------------------------------------
# Cleaned output files
# ---------------------------------------------------------------------------

CLEANED_AIRBNB_FILE = (
    OUT_DIR / CLEANED_AIRBNB_FILE_NAME
)

CLEANED_BONDS_FILE = (
    OUT_DIR / BONDS_FILE_NAME
)

CLEANED_AIRBNB_SA2_FILE = (
    OUT_DIR / AIRBNB_SA2_FILE_NAME
)

CLEANED_MERGED_DATASET_FILE = (
    OUT_DIR / MERGED_FILE_NAME
)


# ---------------------------------------------------------------------------
# Airbnb file settings
# ---------------------------------------------------------------------------

AIRBNB_FILE_PREFIX = config["airbnb"]["file_prefix"]

AIRBNB_FILE_SUFFIX = config["airbnb"]["file_suffix"]