import os
from constants import *

"""
Project setup checker.

Checks that required directories and files exist and follow
the expected project structure.
"""

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def directory_exists(path):
    """Return True if the directory exists."""
    return os.path.isdir(path)


def file_exists(path):
    """Return True if the file exists."""
    return os.path.isfile(path)


def is_valid_airbnb_filename(filename):
    """
    Check whether a filename matches listings-yy-mm.csv.

    Both yy and mm must contain only digits.
    """

    if not filename.startswith(AIRBNB_FILE_PREFIX):
        return False

    if not filename.endswith(AIRBNB_FILE_SUFFIX):
        return False

    name = filename[:-4]  # remove .csv

    parts = name.split("-")

    if len(parts) != 3:
        return False

    prefix, yy, mm = parts

    if prefix != "listings":
        return False

    if not (yy.isdigit() and mm.isdigit()):
        return False

    return True


def create_required_directories():
    """Create the required project directories if missing."""

    required_directories = [
        DATA_DIR,
        UNCLEANED_AIRBNB_DIR,
        CLEANED_DIR,
    ]

    for directory in required_directories:
        if not directory_exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")


def check_directories():
    """Check that the required directories exist."""

    missing = []

    for directory in (
        DATA_DIR,
        UNCLEANED_AIRBNB_DIR,
        CLEANED_DIR,
    ):
        if not directory_exists(directory):
            missing.append(directory)

    return missing


def check_required_files():
    """Check for the required bonds file and Airbnb CSV files."""

    problems = []

    if not file_exists(UNCLEANED_BONDS_FILE):
        problems.append(
            f"Missing required file: {UNCLEANED_BONDS_FILE}"
        )

    if not directory_exists(UNCLEANED_AIRBNB_DIR):
        problems.append(
            f"Missing directory: {UNCLEANED_AIRBNB_DIR}"
        )
        return problems

    csv_files = [
        f for f in os.listdir(UNCLEANED_AIRBNB_DIR)
        if f.lower().endswith(".csv")
    ]

    if len(csv_files) != EXPECTED_AIRBNB_FILE_COUNT:
        problems.append(
            f"Expected {EXPECTED_AIRBNB_FILE_COUNT} Airbnb CSV files "
            f"but found {len(csv_files)}"
        )

    for filename in csv_files:
        if not is_valid_airbnb_filename(filename):
            problems.append(
                f"Invalid Airbnb filename: {filename}"
            )

    return problems


def warn_about_extra_items():
    """
    Print warnings about files and folders that are not part of
    the expected structure.
    """

    expected_data_items = {
        os.path.basename(UNCLEANED_AIRBNB_DIR),
        os.path.basename(UNCLEANED_AIRBNB_FILE),
        os.path.basename(UNCLEANED_BONDS_FILE),
        os.path.basename(CLEANED_DIR)
    }

    if not directory_exists(DATA_DIR):
        return

    unexpected_files = []

    for item in os.listdir(DATA_DIR):
        if item not in expected_data_items:
            unexpected_files.append(item)

    if len(unexpected_files) > 0:
        print(
            f"WARNING: Found the following extra item(s) in {DATA_DIR}.\n    ",
            f"{",\n    ".join(unexpected_files)}\n",
            "These files may be old, unused, or outdated. Consider renaming them or using the other scripts to generate the datasets from scratch.",
            sep = ""
        )


def validate_project():
    """Run all project validation checks."""

    print("Checking project structure...")
    print()

    missing_directories = check_directories()

    if missing_directories:
        print("Required directories are missing:")

        for directory in missing_directories:
            print(f"  - {directory}")

        print()

        answer = input(
            "Create the missing directories now? (y/n): "
        ).strip().lower()

        if answer == "y":
            create_required_directories()
        else:
            print("Project setup was not completed.")
            return False

    print()
    print("Checking required files...")

    file_problems = check_required_files()

    if file_problems:
        print()

        for problem in file_problems:
            print(f"ERROR: {problem}")

        print()
        print(
            "Required CSV files must be added manually."
        )
        return False

    print("All required files were found.")

    print()
    warn_about_extra_items()

    print()
    print("Project structure check passed.")

    return True


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    validate_project()
