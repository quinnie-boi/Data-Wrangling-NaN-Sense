# Deliverable 6 Design Principles document

Draft document: see for my comments/edits --> will update this md file during our

group meeting tomorrow



## Design Principles for the Airbnb and Tenancy Bond Data Pipeline

AI used: M365 Copilot, based on the GPT-5 chat model.

### 1. Pipeline Inputs

The pipeline uses three main data sources to compare short-term Airbnb accommodation with residential rental properties at the SA2 geographic level.

**Airbnb listings and review data**

The first input consists of Airbnb listing and review data from October 2025 to June 2026. Because the Airbnb information is provided separately for different months, the data must first be combined to create a dataset covering the complete study period.

The Airbnb data provides information about properties operating as short-term accommodation. Relevant information is retained for identifying listings, their locations, and their activity during the selected period.

**Tenancy bond data**

The second input is tenancy bond data containing SA2 information. This provides information about residential rental properties and allows the rental market to be compared with Airbnb activity.

Only tenancy records relevant to the October 2025 to June 2026 study period are required. The full dataset is therefore filtered before further processing.

**Stats NZ SA2 geographic data**

The final input is Stats NZ SA2 area codes and geographic information. SA2 areas provide a common geographic unit that can be used to associate records from the Airbnb and tenancy datasets with the same locations.

Geographic information obtained from Stats NZ is used to ensure that locations are identified consistently when the datasets are combined.

### 2. Pipeline Outputs

The main output of the pipeline is a combined dataset that can be used to determine how many rental properties and Airbnb properties are located within the same geographic areas.

The final output should allow the number of Airbnb listings and residential rental properties to be compared by SA2 area. This makes it possible to analyse the relationship between short-term accommodation and conventional rental properties within a consistent geographic unit.

Where appropriate, the processed data should contain information such as:

* SA2 area code
* SA2 area name
* Number of Airbnb listings
* Number of residential rental properties
* Other counts or measures required for subsequent analysis

Keeping SA2 identifiers in the final output also allows the results to be linked back to geographic information for later analysis or visualisation.

### 3. Main Pipeline Steps

The pipeline is divided into a series of stages so that the transformation from the original source data to the final combined dataset can be followed and tested.

**Step 1: Concatenate Airbnb listing data**

The monthly Airbnb datasets covering October 2025 through June 2026 are combined into one dataset.

Before concatenation, the datasets should be checked to ensure that their column names and data formats are compatible. Combining the monthly files at the beginning of the pipeline provides a single dataset that can then be processed consistently.

Where necessary, a column identifying the month or source file should be retained so that the origin of individual observations can still be determined.

**Step 2: Clean the Airbnb data**

The combined Airbnb dataset is cleaned to remove or correct information that is not suitable for the analysis.

Cleaning may include, depending on what was actually required by the source data:

* Removing columns that are not required for the analysis.
* Handling missing values in important fields.
* Removing invalid or unusable records.
* Checking for duplicated records or listings.
* Converting columns to appropriate data types.
* Standardising inconsistent values.
* Checking latitude and longitude values used for geographic matching.
* Retaining only records relevant to the required analysis.

An important design principle is that cleaning operations should be explicit and reproducible. Rather than manually modifying the input files, the cleaning should be performed by the pipeline so that the same rules are applied whenever it is run.

Note: In your submitted version, only list cleaning operations you actually performed. For example, do not claim that duplicates were removed if your code never removes them.

**Step 3: Subset the tenancy bond data**

The original tenancy bond dataset is filtered to create a subset corresponding to the same October 2025 to June 2026 period represented by the Airbnb data.

Using the same period makes the datasets more comparable and prevents tenancy information from unrelated periods from affecting the analysis.

Filtering early also reduces the volume of data that later stages of the pipeline need to process.

**Step 4: Clean the tenancy bond subset**

The resulting tenancy data is then cleaned before being joined with the other datasets.

Relevant cleaning may include:

* Removing unnecessary columns.
* Handling missing SA2 identifiers or other important fields.
* Standardising column names and formats.
* Converting dates and numeric columns to appropriate data types.
* Checking for invalid records.
* Checking duplicate records where appropriate.
* Ensuring SA2 values use the same representation as those obtained from Stats NZ.

Particular attention should be given to the fields used for joining datasets. Differences such as numeric versus string SA2 identifiers could prevent otherwise matching records from joining successfully.

**Step 5: Obtain SA2 geographic data**

SA2 area codes and associated geographic information are obtained using a Stats NZ API.

The geographic information provides a consistent method for identifying the SA2 area associated with the source data. The returned API data should be reduced to the fields needed by the pipeline and converted into a format suitable for joining with the Airbnb and tenancy data.

This stage should also handle API results independently from the main analytical logic where possible. This separation means that retrieving data and processing data remain distinct responsibilities.

**Step 6: Join the Airbnb and tenancy datasets**

Once the datasets have been cleaned and geographic identifiers have been established, the Airbnb and tenancy data can be joined using their common SA2 information.

Rather than joining individual rental properties directly to individual Airbnb listings, the data can be grouped or aggregated by SA2 area, depending on the required analysis. Counts can then be calculated for each geographic area.

For example, the final dataset could conceptually contain:

Plain Text

SA2 code | SA2 name | Airbnb count | Rental property count

Show more lines

This produces a consistent dataset from which rental and Airbnb activity within the same locations can be compared.

### 4. Coding and Software Design Strategies

The pipeline will follow several coding and software design practices discussed in lectures, with an emphasis on making the project organised, reproducible, understandable, and easy to modify. A key principle is the clear separation of data, code, and output. Original datasets, including the Airbnb listings, tenancy bond data, and Stats NZ geographic data, will be stored separately from the scripts used to process them. Files generated by the pipeline will be stored in an output directory. This follows the principle of Data + Code → Output, where the data and code form the consistent and permanent components of the project, while outputs can be regenerated when required. Data and code can therefore be committed to Git, while temporary or reproducible outputs generally do not need to be version controlled.

Another important principle is that the original source data will not be manually edited. The Airbnb, tenancy bond, and Stats NZ data will be retained in their original form, with cleaning and transformation carried out through code. For example, filtering the tenancy data to the October 2025 to June 2026 study period and cleaning the Airbnb listings will be performed by scripts rather than by changing the original files. Preserving the raw data creates a clear audit trail because every change made to the data is represented in the code. It also makes the project easier to modify or extend because the pipeline can always be rerun from the original source data using updated processing rules.

The project will also use relative file paths, with the project root treated as the working directory. Rather than using absolute paths that refer to a specific location on one computer, scripts will locate files relative to the project root, such as data/airbnb/listings.csv. The code will not use commands such as os.chdir() to change the working directory. This makes the project more portable because the entire project folder can be moved to another location or computer without requiring file paths within the scripts to be rewritten.

The pipeline will be organised using multiple small files with clearly defined tasks rather than one large script containing every processing step. Separate scripts can be responsible for tasks such as concatenating the monthly Airbnb files, cleaning the Airbnb data, creating the tenancy subset, cleaning the tenancy data, retrieving SA2 geographic information, and joining the final datasets. Breaking the pipeline into smaller components makes each stage easier to understand and debug. It also improves flexibility because individual components can be modified or reused without necessarily changing the rest of the pipeline.

Each component of the pipeline will have a clear interface, meaning that its required inputs and expected outputs will be identifiable. For example, the Airbnb cleaning stage will take the concatenated Airbnb data as its input and produce cleaned Airbnb data as its output. Similarly, the final joining stage will take the cleaned Airbnb data, cleaned tenancy data, and SA2 information as inputs and produce the combined SA2-level dataset. Defining clear inputs and outputs makes the relationship between pipeline stages easier to understand and reduces dependencies between different parts of the project.

Important parameters will also be made visible rather than being hidden throughout the code. Values that control the behaviour of the pipeline, such as the beginning and end of the study period, input and output filenames, and other configuration values, will be defined clearly near the beginning of the relevant scripts and given meaningful names. For example, defining the study period as START\_DATE and END\_DATE makes its purpose clearer than repeatedly placing date values directly inside the processing code. This avoids the use of unexplained magic numbers or values and makes future modifications easier because important settings can be found and changed in a predictable location.

Files will use consistent headers to make their purpose and requirements clear. Where appropriate, the beginning of each script will contain a short description of what the file does, followed by library imports, parameters, and the loading of required inputs. This effectively provides a simple description of the script's interface and allows another person examining the project to quickly understand its role within the overall pipeline.

Finally, the project will aim to use self-documenting code. File names, function names, and variable names will be chosen to describe their purpose clearly, reducing the need for excessive comments. Names such as airbnb\_listings, tenancy\_subset, and sa2\_area\_code communicate considerably more information than generic names such as df1, data, or temp. Comments will still be used where they provide useful context, particularly where it is necessary to explain why a particular transformation or decision has been made. Together, these practices should make the pipeline easier for both the original developer and another programmer to understand, audit, reproduce, and maintain.

**AI Declaration**

M365 Copilot, based on the GPT-5 chat model, was used to assist with organising, drafting, and refining this design principles document.
