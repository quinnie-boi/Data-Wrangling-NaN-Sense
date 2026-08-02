# DATA201/422 Data-Wrangling

# Deliverable 2
The listings.csv dataset is stored locally under `deliverable_2/data/listings.csv`. The contents of folders named `data` is excluded from being uploaded to git, with an entry in our `.gitignore`.

## AirBnB Dataset
Discovery - [The contents of the dataset](docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit?pli=1&gid=1322284596#gid=1322284596) are available from AirBnB

The data is in a somewhat cleaned and structured format by AirBnB, but not necessarily in the way we want.


|    Variable        | Type  |  Description |
|--------------------|---|------------------|
| id                 | int   | airbnb's unique identifier for each listing |
| name               | text  | name of listing |
| host_id            | int   | unique identifier of the host/user. The identifier is unique for a given host, not unique in  dataset. |
| host_name          | text  | name of the host, typically only first name |
| neighbourhood_group| text  | calculated name of the region when reverse geocoded from the latitude and longitude as defined by open or public digital shapefiles. |
| neighbourhood      | text  | name of the neighbourhood the listing is in |
| latitude           | float | coordinate location |
| longitude          | float | coordinate location |
| room_type          | text  | one of [Entire home/apt\|Private room\|Shared room\|Hotel] |
| price              | int   | price in NZD |
| minimum_nights     | int   | minimum length stay for listing |
| number_of_reviews  | int   | self explanatory |
| last_review        | text  | date of last (newest) review |
| reviews_per_month  | float | calculated #reviews in a month, since first review (exact formula in docs) |
| calculated_host_listings_count | int | # of listings the host has in the city/region |
| availabilty_365    | int   | unclear to me. Docs say "avaliability_x. The availability of the listing x days in the future as determined by the calendar. Note a listing may not be available because it has been booked by a guest or blocked by the host." |
| number_of_reviews_ltm | int | # of reviews listing has in the last 12 months |
| license            | text  | license/permit/registration number - appears to be entirely empty column in our dataset |
