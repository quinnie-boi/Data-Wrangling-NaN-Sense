import pandas as pd
from constants import CLEANED_AIRBNB_FILE

sa2 = pd.read_csv("data/chch_with_sa2.csv")
airbnb = pd.read_csv(CLEANED_AIRBNB_FILE)

key = 'id'
airbnb = pd.merge(airbnb, sa2[[key, 'sa2_code']], on = key, how = 'left'  )
print(airbnb['sa2_code'].summary())
print(sa2['sa2_code'].summary())

airbnb.to_csv(CLEANED_AIRBNB_FILE.replace(".csv", "_sa2.csv"))
