# DATA201/422 Data-Wrangling
# Deliverable 5
from start to finish:
the number in each file indicates the deliverable it relates to
1. setup_project.py
2. summary_stats_2.py (optional)
3. merge_listings_3.py (merges the 9 listing files)
4. clean_datasets_4.py (cleans both datasets)
5. add_sa2_codes_v5b.py (adds sa2 codes to cleaned AirBnb dataset)
6. main_5.py (Performs the other deliverable 5 tasks)


# Deliverable 4
## Detailed quarterly report, 2020-2026 of rental bond data
Rental bond data from dwellings rented by private landlords
note: The files are updated each month and do not include the most recent month’s data, for example files released in 
July will contain information up to the end of May

It is listed by tenancy start date and uses the [SA2-2019 area definitions](https://datafinder.stats.govt.nz/layer/98970-statistical-area-2-2019-generalised/) from Statistics NZ
Privacy protection measures have been applied; fixed random rounding is applied to [base 3](https://bayesiandemography.github.io/poputils/reference/rr3.html#details) and there is a suppression of results when there are fewer than 5 bonds for any given selection.
Discovery - [https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/] 
Source credit: 'The Ministry of Business, Innovation and Employment'

| Variable                | Type  | Description                                                                                                                                | Keep | Reason                                     |
|-------------------------|-------|--------------------------------------------------------------------------------------------------------------------------------------------|:----:|--------------------------------------------|
| TimeFrame               | date  | Date ended for quarter in which bond was lodged                                                                                            |  ✅   | Comparison with other dataset              |
| Location Id             | float | SA2-2019 area code                                                                                                                         |  ✅   | To be compared with the Airbnb locations   |
| DwellingType            | text  | one of [Apartment\|Boarding House\|Flat\|House\|Room]                                                                                      |  ✅   | keep for visual analysis/comparison        |
| Number Of Beds          | float | Meant to be one of [1, 2, 3, 4, 5+]. Actually one of [0,1,2,3,4,5,6,7,8,9,15,5+ ALL, NA] Number of bedrooms in dwelling of bond registered |  ✅   | ""                                         |
| Total Bonds             | float |                                                                                                                                            |  ❌   | Do not need for Airbnb comparison          |
| Active Bonds            | float | Number of active bonds at end of quarter                                                                                                   |  ❌   | ""                                         |
| Closed Bonds            | float | Number of bonds closed/returned in the quarter                                                                                             |  ❌   | ""                                         |
| Median Rent             | float | Median rent for dwellings in the quarter                                                                                                   |  ✅   | compare to airbnb med values               |
| Geometric Mean          | float | Calculated by multiplying values together and taking the nth root of the result                                                            |  ✅   | "" geom-mean (to be calculated?) values "" |
| Upper Quartile Rent     | float | Rents above this figure are in the top 25% of rents for this area in the quarter                                                           |  ✅   | "" quartiles ""                            |
| Lower Quartile Rent     | float | Rents bellow this figure are in the top 25% of rents for this area in the quarter                                                          |  ✅   | "" quartiles ""                            |
| Log Std Dev Weekly Rent | int   | STD DEV of weekly rent                                                                                                                     |  ✅   | Assume useful for variance analysis        |



## Weird NA/Null values in Quarterly.
Since NA and NULL never appear in the same column we can replace both with NA. They may have different semantic meanings but that information won't be lost. 
`Location ID` contains both 794 `NULL` values and 1091 special `-99` values. It is otherwise a non-negative six-digit number.

The NA values in `Location ID`, `Median Rent`, `Geometric Mean Rent`, `Upper Quartile Rent`, `Lower Quartile Rent`, and `Log Std Dev Weekly Rent`always appear in the same row. Which means there are 803 rows with mostly `NA` or `NULL` values.

For `Location ID`: (#missing - #NULL) = 1885-794 = 1091. There were 1091 rows left after dropping NA values from the other 5 rows, so they are linked.


| Column                  | NA count | Null Count | 
|-------------------------|----------|------------|
| TimeFrame               | 0        | 0          |
| Location Id 	           | 0        | 794        |
| Dwelling Type           | 0        | 0          |
| Number of Beds          | 12009    | 0          |
| Total Bonds 	           | 0        | 0          |
| Active Bonds            | 0        | 0          |
| Closed Bonds            | 0        | 0          |
| Median Rent             | 0        | 803        |
| Geometric Mean Rent 	   | 0        | 803        |
| Upper Quartile Rent 	   | 0        | 803        |
| Lower Quartile Rent     | 0        | 803        |
| Log Std Dev Weekly Rent | 0        | 859        |

Statistics of rows where `Location Id` == -99 vs the entire dataset vary drastically.
```
         Location Id    Total Bonds   Active Bonds   Closed Bonds    Median Rent  Geometric Mean Rent  Upper Quartile Rent  Lower Quartile Rent  Log Std Dev Weekly Rent
count         1091.0     1091.00000    1091.000000    1091.000000    1091.000000          1091.000000          1091.000000          1091.000000              1091.000000
mean           -99.0     3804.00275   42546.140238    3308.744271     541.318973           520.241063           653.245646           439.442713                 0.390562
std              0.0     7733.17921   86592.250320    6630.456243     218.261322           198.211433           257.078213           182.982175                 0.187875
min            -99.0        6.00000       3.000000       0.000000     135.000000           146.000000           154.000000           125.000000                 0.047700
25%            -99.0       60.00000     606.000000      57.000000     375.000000           361.000000           460.000000           291.500000                 0.305650
50%            -99.0      948.00000   11163.000000     807.000000     520.000000           510.000000           620.000000           420.000000                 0.360000
75%            -99.0     3877.50000   47565.000000    3480.000000     661.500000           634.000000           800.000000           550.000000                 0.425900
max            -99.0    49875.00000  520821.000000   48384.000000    1140.000000          1133.000000          1295.000000           963.000000                 3.234200
         Location Id    Total Bonds   Active Bonds   Closed Bonds    Median Rent  Geometric Mean Rent  Upper Quartile Rent  Lower Quartile Rent  Log Std Dev Weekly Rent
count  225286.000000  226080.000000  226080.000000  226080.000000  225277.000000        225277.000000        225277.000000        225277.000000            225221.000000
mean   209944.790466      33.807604     358.413973      27.973806     574.009837           564.424433           635.220209           516.974827                 0.215372
std     79061.243519     600.844842    6755.815227     515.108357     167.703344           167.589406           194.942332           156.214997                 0.167486
min       -99.000000       6.000000       0.000000       0.000000       0.000000             0.000000             0.000000             0.000000                 0.000000
25%    141500.000000       6.000000      48.000000       3.000000     475.000000           461.000000           520.000000           420.000000                 0.107200
50%    192800.000000       9.000000      93.000000       9.000000     570.000000           558.000000           620.000000           518.000000                 0.170300
75%    253100.000000      15.000000     165.000000      15.000000     660.000000           655.000000           728.000000           603.000000                 0.276500
max    363300.000000   49875.000000  520821.000000   48384.000000    3350.000000          2818.000000          3625.000000          2785.000000                 5.886000
```


## Airbnb Dataset
Discovery - [The contents of the dataset](https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?pli=1&gid=1322284596#gid=1322284596) are available from Airbnb

| Variable                       | Type  | Description                                                                                                                                                                                                                     | Keep | Reason                                                                                                |
|--------------------------------|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------|-------------------------------------------------------------------------------------------------------|
| id                             | int   | airbnb's unique identifier for each listing                                                                                                                                                                                     | ✅    |                                                                                                       |
| name                           | text  | name of listing                                                                                                                                                                                                                 | ❌    | We do not care about how people advertise their rental.                                               |
| host_id                        | int   | unique identifier of the host/user. The identifier is unique for a given host, not unique in  dataset.                                                                                                                          | ✅    |                                                                                                       |
| host_name                      | text  | name of the host, typically only first name                                                                                                                                                                                     | ❌    | We are not interested in the statistics of renter's names.                                            |
| neighbourhood_group            | text  | calculated name of the region when reverse geocoded from the latitude and longitude as defined by open or public digital shapefiles. Mostly contains Districts and Cities                                                       | ❌    | Always equal to "Christchurch City" in our filtered dataset                                           |
| neighbourhood                  | text  | name of the neighbourhood the listing is in. Mostly contains wards                                                                                                                                                              | ✅    | Good for analysing by suburb/ward.                                                                    |
| latitude                       | float | coordinate location                                                                                                                                                                                                             | ✅    |                                                                                                       |
| longitude                      | float | coordinate location                                                                                                                                                                                                             | ✅    |                                                                                                       |
| room_type                      | text  | one of [Entire home/apt\|Private room\|Shared room\|Hotel]                                                                                                                                                                      | ✅    |                                                                                                       |
| price                          | int   | price in NZD                                                                                                                                                                                                                    | ✅    |                                                                                                       |
| minimum_nights                 | int   | minimum length stay for listing                                                                                                                                                                                                 | ❌    | Could plausibly be kept for some *very* specific analysis. But seems unlikely. Has 328 NAs.           |
| number_of_reviews              | int   | self explanatory                                                                                                                                                                                                                | ✅    |                                                                                                       |
| last_review                    | text  | date of last (newest) review                                                                                                                                                                                                    | ✅    |                                                                                                       |
| reviews_per_month              | float | calculated #reviews in a month, since first review (exact formula in docs)                                                                                                                                                      | ❌    | Calculated stat from other columns. Has 43617 missing values despite `number_of_reviews` having none. |
| calculated_host_listings_count | int   | #listings the host has in the city/region                                                                                                                                                                                   | ✅    |                                                                                                       |
| availabilty_365                | int   | unclear to me. Docs say "avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host." | ✅    |                                                                                                       |
| number_of_reviews_ltm          | int   | #reviews listing has in the last 12 months                                                                                                                                                                                  | ✅    |                                                                                                       |
| license                        | text  | license/permit/registration number - appears to be entirely empty column in our dataset                                                                                                                                         | ❌    | Always empty                                                                                          |
# Workflow and Using Git
There is a helpful document included called `using_git.md` which gives a brief overview of some useful commands.
 
# Project Setup
 
Before running the project, make sure the following folders exist:
 
```
data/
data/uncleaned_airbnb_listings/
data/cleaned/
```

The following files must also be added manually:

```
data/uncleaned_bonds.csv
data/uncleaned_airbnb_listings/listings-yy-mm.csv
```

There should be nine Airbnb CSV files, and each file must follow the naming format:

```
listings-yy-mm.csv
```
where `yy-mm` is a the year and month as numbers.

## To check that your project data is set up correctly, run:
```bash
python setup_project.py
```

This script will:

 - Check that the required folders exist.
 - Offer to create any missing folders.
 - Check that the required CSV files exist.
 - Verify the Airbnb file naming convention.
 - Warn about any extra files or folders that may be out of date.

> [!IMPORTANT]
> The required CSV files are not created automatically and must be downloaded and renamed manually.
