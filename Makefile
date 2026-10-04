.PHONY: all

AIRBNB_FILES := $(wildcard data/uncleaned_airbnb_listings/listings-*.csv)

all: data/cleaned/merged_listings_and_bonds.csv out/chch_number_of_reviews.png

data/uncleaned_airbnb_listings.csv: merge_listings_3.py $(AIRBNB_FILES)
	python merge_listings_3.py

data/cleaned/chch_airbnb_listings.csv: clean_datasets_4.py data/uncleaned_airbnb_listings.csv data/uncleaned_bonds.csv
	python clean_datasets_4.py
data/cleaned/chch_airbnb_listings_with_sa2.csv: add_sa2_codes_v5b.py data/cleaned/chch_airbnb_listings.csv
	python add_sa2_codes_v5b.py
data/cleaned/merged_listings_and_bonds.csv: main_5.py data/cleaned/chch_airbnb_listings_with_sa2.csv data/cleaned/tenancy_bonds.csv
	python main_5.py
out/chch_number_of_reviews.png: summary_statistics_2.py data/cleaned/chch_airbnb_listings.csv
	python summary_statistics_2.py