import pandas as pd

def med_airbnb_price(location_id, filename):
    """Returns the median Airbnb price in a dataset for a given location,
    excludes blank or missing prices."""
    
    #Loads dataset
    df = pd.read_csv(filename)
    
    #Filters to the specified sa2_code associated to the location_id parameter (e.g. 326600)
    df = df[df["sa2_code"] == location_id]

    #Pandas median() function ignores existing Not-a-Number (NaN) values, but will not convert blanks or text into NaN.
    #The entire price column appears numeric, so this line is likely not necessary, but if you get an error, use the
    # line below to convert non-numeric price entries to NaN so they are also excluded from the calculation.
    
    #df["price"] = pd.to_numeric(df["price"], errors="coerce")
    
    #Returns median price
    return df["price"].median()

#Example to test for week 9 deliverable
median_price = med_airbnb_price(326600,"chch_airbnb_bond_with_sa2_names.csv")
print(f"Median Airbnb price for location_id 326600: ${median_price:.2f}")