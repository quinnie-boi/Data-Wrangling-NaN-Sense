.PHONY: all clean

PYTHON = .venv/bin/python

# ---------------------------------------------------------------------------
# Raw input files
# ---------------------------------------------------------------------------

AIRBNB_RAW = $(wildcard data/uncleaned_airbnb_listings/listings-*.csv)
RAW_BONDS = data/uncleaned_bonds.csv


# ---------------------------------------------------------------------------
# Generated datasets
# ---------------------------------------------------------------------------

UNCLEANED_AIRBNB = out/uncleaned_airbnb_listings.csv
CLEANED_AIRBNB = out/chch_airbnb_listings.csv
CLEANED_BONDS = out/cleaned_bonds.csv
AIRBNB_SA2 = out/cleaned_airbnb_with_sa2.csv
MERGED_DATA = out/merged_listings_and_bonds.csv


# ---------------------------------------------------------------------------
# Generated figures
# ---------------------------------------------------------------------------

REVIEWS_PLOT = out/chch_number_of_reviews.png


# ---------------------------------------------------------------------------
# Build everything
# ---------------------------------------------------------------------------

all: $(MERGED_DATA) $(REVIEWS_PLOT)


# ---------------------------------------------------------------------------
# 01 - Merge raw Airbnb listing files
# ---------------------------------------------------------------------------

$(UNCLEANED_AIRBNB): src/01-merge-listings.py $(AIRBNB_RAW) constants.py config.yaml
    PYTHONPATH=. $(PYTHON) src/01-merge-listings.py


# ---------------------------------------------------------------------------
# 02 - Clean Airbnb and Rental Bond datasets
# ---------------------------------------------------------------------------

$(CLEANED_AIRBNB) $(CLEANED_BONDS) &: src/02-clean-datasets.py $(UNCLEANED_AIRBNB) $(RAW_BONDS) constants.py config.yaml
    PYTHONPATH=. $(PYTHON) src/02-clean-datasets.py

# ---------------------------------------------------------------------------
# 03 - Add SA2 codes to Airbnb
# ---------------------------------------------------------------------------

$(AIRBNB_SA2): src/03-add-sa2-v5b.py $(CLEANED_AIRBNB) constants.py config.yaml
    PYTHONPATH=. $(PYTHON) src/03-add-sa2-v5b.py


# ---------------------------------------------------------------------------
# 04 - Merge Airbnb and Rental Bond datasets
# ---------------------------------------------------------------------------

$(MERGED_DATA): src/04-main-5.py $(AIRBNB_SA2) $(CLEANED_BONDS) constants.py config.yaml
    PYTHONPATH=. $(PYTHON) src/04-main-5.py


# ---------------------------------------------------------------------------
# 05 - Summary statistics / figures
# ---------------------------------------------------------------------------

$(REVIEWS_PLOT): src/05-summary-statistics.py $(CLEANED_AIRBNB) constants.py config.yaml
    PYTHONPATH=. $(PYTHON) src/05-summary-statistics.py


# ---------------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------------

clean:
	rm -f $(UNCLEANED_AIRBNB)
	rm -f $(CLEANED_AIRBNB)
	rm -f $(CLEANED_BONDS)
	rm -f $(AIRBNB_SA2)
	rm -f $(MERGED_DATA)
	rm -f $(REVIEWS_PLOT)