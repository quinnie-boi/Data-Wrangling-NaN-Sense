# DATA201/422 Data-Wrangling
# Deliverable 4
> [!WARNING]
> Please move the downloaded csv listings into /data/raw. This will keep them separate from the combined and cleaned

## Detailed quarterly report, 2020-2026 of rental bond data
Rental bond data from dwellings rented by private landlords
note: The files are updated each month and do not include the most recent month’s data, for example files released in 
July will contain information up to the end of May
Discovery - [https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/]

> It is listed by tenancy start date and uses the [SA2-2019 area definitions](https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/) from Statistics NZ
> Privacy protection measures have been applied; fixed random rounding is applied to [base 3](https://bayesiandemography.github.io/poputils/reference/rr3.html#details) and there is a suppression of results when there are fewer than 5 bonds for any given selection.


| Variable                | Type  | Description                                                                       |
|-------------------------|-------|-----------------------------------------------------------------------------------|
| TimeFrame               | date  | Date ended for quarter in which bond was lodged                                   |
| Location Id             | float | SA2-2019 area code                                                                |
| DwellingType            | text  | Type of accomodation (room, flat, etc)                                            |
| Number Of Beds          | float | (mixed??) Number of bedrooms in dwelling of bond registered                       |
| Total Bonds             | float |                                                                                   |
| Active Bonds            | float | Number of active bonds at end of quarter                                                                                  |
| Closed Bonds            | float | Number of bonds closed/returned in the quarter                                    |
| Median Rent             | float | Median rent for dwellings in the quarter                                          |
| Geometric Mean          | float | Calculated by multiplying values together and taking the nth root of the result   |
| Upper Quartile Rent     | float | Rents above this figure are in the top 25% of rents for this area in the quarter  |
| Lower Quartile Rent     | float | Rents bellow this figure are in the top 25% of rents for this area in the quarter |
| Log Std Dev Weekly Rent | int   | STD DEV of weekly rent                                                                                  |

## Weird NA/Null values in Quarterly.
Since NA and NULL never appear in the same column we can replace both with NA. They may have different semantic meanings but that information won't be lost. 
`Location ID` contains both 794 `NULL` values and 1091 special `-99` values. It is otherwise a non-negative six digit number.

The NA values in `Location ID`, `Median Rent`, `Geometric Mean Rent`, `Upper Quartile Rent`, `Lower Quartile Rent`, and `Log Std Dev Weekly Rent`always appear in the same row. Which means there are 803 rows with mostly `NA` or `NULL` values.

For `Location ID`: (#missing - #NULL) = 1885-794 = 1091. There were 1091 rows left after dropping NA values from the other 5 rows, so they are linked.


| Column | NA count | Null Count | 
| --- | --- | --- |
| TimeFrame 			| 0 | 0 |
| Location Id 			| 0 | 794 |
| Dwelling Type 		| 0 | 0 |
| Number of Beds		| 12009 | 0 |
| Total Bonds 			| 0 | 0 |
| Active Bonds 			| 0 | 0 |
| Closed Bonds 			| 0 | 0 |
| Median Rent 			| 0 | 803 |
| Geometric Mean Rent 	| 0 | 803 |
| Upper Quartile Rent 	| 0 | 803 |
| Lower Quartile Rent	| 0 | 803 |
| Log Std Dev Weekly Rent| 0 | 859 |

## AirBnB Dataset
Discovery - [The contents of the dataset](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?pli=1&gid=1322284596#gid=1322284596) are available from AirBnB

|    Variable        | Type  |  Description | Keep | Reason |
|--------|---|------------------|-|--------|
| id                 | int   | airbnb's unique identifier for each listing |✅|
| name               | text  | name of listing |❌| We do not care about how people advertise their rental. |
| host_id            | int   | unique identifier of the host/user. The identifier is unique for a given host, not unique in  dataset. |✅|
| host_name          | text  | name of the host, typically only first name |❌| We are not interested in the statistics of renter's names.
| neighbourhood_group| text  | calculated name of the region when reverse geocoded from the latitude and longitude as defined by open or public digital shapefiles. Mostly contains Districts and Cities |✅|
| neighbourhood      | text  | name of the neighbourhood the listing is in. Mostly contains wards |❌| Too small-scale for analysis? |
| latitude           | float | coordinate location |✅|
| longitude          | float | coordinate location |✅|
| room_type          | text  | one of [Entire home/apt\|Private room\|Shared room\|Hotel] |✅|
| price              | int   | price in NZD |✅|
| minimum_nights     | int   | minimum length stay for listing |❌| Could plausibly be kept for some *very* specific analysis. But seems unlikely. Has 328 NAs. |
| number_of_reviews  | int   | self explanatory |✅|
| last_review        | text  | date of last (newest) review |✅|
| reviews_per_month  | float | calculated #reviews in a month, since first review (exact formula in docs) |❌| Calculated stat from other columns. Has 43617 missing values despite `number_of_reviews` having none. |
| calculated_host_listings_count | int | # of listings the host has in the city/region |✅|
| availabilty_365    | int   | unclear to me. Docs say "avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host." |✅|
| number_of_reviews_ltm | int | # of reviews listing has in the last 12 months |✅|
| license            | text  | license/permit/registration number - appears to be entirely empty column in our dataset |❌| Always empty |

# Usage
The naming convention needed for our code to work is "listings-yy-mm.cvs" e.g. listings-26-01 for January 2026

The listings.csv dataset is stored locally under `deliverable_2/data/listings.csv`. The contents of folders named `data` is excluded from being uploaded to git, with an entry in our `.gitignore`.


