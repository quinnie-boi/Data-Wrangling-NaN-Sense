# Design Principles for the Airbnb and Tenancy Bond Data Pipeline

**AI used: M365 Copilot, based on the GPT-5 chat model.**

## 1. Pipeline Inputs

The pipeline uses three main data sources to compare short-term Airbnb accommodation with residential rental properties at the SA2 geographic level.

### Airbnb listings and review data

The first input consists of Airbnb listing and review data from October 2025 to June 2026. Because the Airbnb information is provided separately for different months, the data must first be combined to create a dataset covering the complete study period.

The Airbnb data provides information about properties operating as short-term accommodation. Relevant information is retained for identifying listings, their locations, and their activity during the selected period.

### Tenancy bond data

The second input is tenancy bond data containing SA2 information. This provides information about residential rental properties and allows the rental market to be compared with Airbnb activity.

Only tenancy records relevant to the October 2025 to June 2026 study period are required. The full dataset is therefore filtered before further processing.

### Stats NZ SA2 geographic data

The final input is Stats NZ SA2 area codes and geographic information. SA2 areas provide a common geographic unit that can be used to associate records from the Airbnb and tenancy datasets with the same locations.

Geographic information obtained from Stats NZ is used to ensure that locations are identified consistently when the datasets are combined.

## 2. Pipeline Outputs

The main output of the pipeline is a combined dataset that can be used to compare Airbnb activity and residential rental bond activity within the same geographic areas.

The final output should allow Airbnb listings and rental bond data to be compared by SA2 area. This makes it possible to analyse the relationship between short-term accommodation and rental activity within a consistent geographic unit and across different time periods.

**Where appropriate, the processed data should contain information such as:**

- SA2 area code
- SA2 area name
- Number of Airbnb listings
- Month and year in which the Airbnb listings were recorded
- Airbnb listing prices
- Number of active rental bonds per SA2 area per quarter
- Number of closed rental bonds per SA2 area per quarter
- Quarter and year associated with the rental bond data
- Median weekly rental price per SA2 area
- Geometric mean weekly rental price per SA2 area
- Lower quartile of weekly rental prices per SA2 area
- Upper quartile of weekly rental prices per SA2 area
- Other counts or measures required for subsequent analysis

Keeping the SA2 identifiers and relevant time periods in the final output allows the Airbnb and rental bond datasets to be linked consistently. It also enables the results to be connected back to geographic information for later analysis or visualisation.

## 3. Main Pipeline Steps

The pipeline is divided into a series of stages so that the transformation from the original source data to the final combined dataset can be followed and tested.

### Step 1: Concatenate Airbnb listing data

The monthly Airbnb datasets covering October 2025 through June 2026 are combined into one dataset.

Before concatenation, the datasets should be checked to ensure that their column names and data formats are compatible. Combining the monthly files at the beginning of the pipeline provides a single dataset that can then be processed consistently.

Where necessary, a column identifying the month or source file should be retained so that the origin of individual observations can still be determined.

### Step 2: Clean the Airbnb data

The combined Airbnb dataset is cleaned to remove or correct information that is not suitable for the analysis.

Cleaning may include, depending on what was actually required by the source data:

- Removing columns that are not required for the analysis.
- Handling missing values in important fields.
- Removing invalid or unusable records.
- Checking for duplicated records or listings.
- Converting columns to appropriate data types.
- Standardising inconsistent values.
- Checking latitude and longitude values used for geographic matching.
- Retaining only records relevant to the required analysis.

An important design principle is that cleaning operations should be explicit and reproducible. Rather than manually modifying the input files, the cleaning should be performed by the pipeline so that the same rules are applied whenever it is run.

### Step 3: Subset the tenancy bond data

The original tenancy bond dataset is filtered to create a subset corresponding to the same October 2025 to June 2026 period represented by the Airbnb data.

Using the same period makes the datasets more comparable and prevents tenancy information from unrelated periods from affecting the analysis.

Filtering early also reduces the volume of data that later stages of the pipeline need to process.

### Step 4: Clean the tenancy bond subset

The resulting tenancy data is then cleaned before being joined with the other datasets.

Relevant cleaning may include:

- Removing unnecessary columns.
- Handling missing SA2 identifiers or other important fields.
- Standardising column names and formats.
- Converting dates and numeric columns to appropriate data types.
- Checking for invalid records.
- Checking duplicate records where appropriate.
- Ensuring SA2 values use the same representation as those obtained from Stats NZ.

Particular attention should be given to the fields used for joining datasets. Differences such as numeric versus string SA2 identifiers could prevent otherwise matching records from joining successfully.

### Step 5: Obtain SA2 geographic data

SA2 area codes and associated geographic information are obtained using a Stats NZ API.

The geographic information provides a consistent method for identifying the SA2 area associated with the source data. The returned API data should be reduced to the fields needed by the pipeline and converted into a format suitable for joining with the Airbnb and tenancy data.

This stage should also handle API results independently from the main analytical logic where possible. This separation means that retrieving data and processing data remain distinct responsibilities.

### Step 6: Join the Airbnb and tenancy datasets

Once the datasets have been cleaned and geographic identifiers have been established, the Airbnb and tenancy data can be joined using their common SA2 information.

Rather than joining individual rental properties directly to individual Airbnb listings, the data can be grouped or aggregated by SA2 area, depending on the required analysis. Counts can then be calculated for each geographic area.

This produces a consistent dataset from which rental and Airbnb activity within the same locations can be compared.

## 4. Coding and Software Design Strategies

The pipeline will follow software design practices that make the project organised, reproducible, and easy to maintain. A key principle is the separation of data, code, and output. Original datasets, including Airbnb listings, tenancy bond data, and Stats NZ geographic data, will be kept separate from processing scripts and generated outputs. This follows the Data + Code → Output principle, allowing outputs to be regenerated when required.

Original source data will not be manually edited. Instead, all cleaning and transformation will be performed through code. For example, scripts will filter tenancy data to the October 2025 to June 2026 period and clean the Airbnb listings. Keeping the raw data unchanged provides an audit trail and allows the pipeline to be rerun if processing requirements change.

The project will use relative file paths from the project root, such as data/airbnb/listings.csv, rather than computer-specific absolute paths. Scripts will also avoid changing the working directory with commands such as os.chdir(). This makes the project easier to move between computers without modifying file paths.

Rather than using one large script, the pipeline will be divided into small components with specific responsibilities. Separate scripts will handle tasks such as combining Airbnb files, cleaning datasets, creating the tenancy subset, retrieving SA2 geographic information, and joining the final datasets. Each component will have clearly defined inputs and outputs, making the pipeline easier to understand, test, and modify.

Important parameters, such as the study period and file locations, will be clearly defined and given meaningful names. For example, START_DATE and END_DATE will be used instead of placing dates directly throughout the processing code. This avoids unexplained values and makes configuration easier to change.

Scripts will also follow a consistent structure, with a brief description followed by imports, parameters, and processing steps. Self-documenting names will be used for files, functions, and variables, such as airbnb_listings, tenancy_subset, and sa2_area_code, rather than generic names such as df1 or temp. Comments will mainly explain the reasoning behind less obvious decisions rather than restating what the code does.

Together, these practices will make the pipeline easier to understand, reproduce, debug, and maintain.

**AI Declaration**

M365 Copilot, based on the GPT-5 chat model, was used to assist with organising, drafting, and refining this design principles document.

## Future Changes

For future revisions of our pipeline, we can make the following chances to better follow the best coding practices that we have learnt from lectures:

Firstly, we would follow the coding practice of separating our pipeline into different folders. This would increase the overall readability of our pipeline as well as making it easier to find specific sections of our pipeline. We would achieve this by seperating our folders into data, inputs and code.

Currently, we have our data folder set up to better sort out our cleaned and uncleaned data and to separate it from the rest of our pipeline files. However, the code and the output folders are still yet to be implemented (implemented for automation deliverable).

Secondly, we would have differently named output files; this will allow the output to be separated via the different output types allowing for easier comprehension of the results. Especially when multiple outputs are given at once.
