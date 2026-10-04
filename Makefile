.PHONY: all clean

PYTHON = .venv/bin/python
PYTHONPATH = .

AIRBNB_RAW = $(wildcard data/uncleaned_listings/*.csv)

UNCLEANED_AIRBNB = out/uncleaned_airbnb.csv
CLEANED_AIRBNB = out/cleaned_airbnb.csv
AIRBNB_SA2 = out/cleaned_airbnb_with_sa2.csv
RAW_BONDS = data/uncleaned_bonds.csv
CLEANED_BONDS = out/cleaned_bonds.csv

all: $(AIRBNB_SA2)


$(UNCLEANED_AIRBNB): $(AIRBNB_RAW) src/01-read-airbnb.py constants.py config.yaml
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/01-read-airbnb.py


$(CLEANED_AIRBNB): $(UNCLEANED_AIRBNB) src/02-clean-airbnb.py constants.py config.yaml
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/02-clean-airbnb.py


$(AIRBNB_SA2): $(CLEANED_AIRBNB) src/03-sa2-noAPI.py constants.py config.yaml
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/03-sa2-noAPI.py

$(CLEANED_BONDS): $(RAW_BONDS) src/05-read-rental-data.py constants.py config.yaml
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/05-read-rental-data.py


clean:
	rm -f $(UNCLEANED_AIRBNB)
	rm -f $(CLEANED_AIRBNB)
	rm -f $(AIRBNB_SA2)