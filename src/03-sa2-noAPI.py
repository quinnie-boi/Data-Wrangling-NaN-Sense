"API credentials not working"
import geopandas as gpd
import pandas as pd
from shapely import wkt

from constants import CLEANED_AIRBNB_FILE, SA2_2019_FILE, CLEANED_AIRBNB_SA2_FILE

# Read Airbnb data
airbnb = pd.read_csv(CLEANED_AIRBNB_FILE)

# Convert Airbnb latitude/longitude to points
airbnb = gpd.GeoDataFrame(
    airbnb,
    geometry=gpd.points_from_xy(
        airbnb["longitude"],
        airbnb["latitude"]
    ),
    crs="EPSG:4326"
)

# Read SA2 polygons
sa2 = pd.read_csv(SA2_2019_FILE)

# Convert WKT text into polygon geometry
sa2["geometry"] = sa2["WKT"].apply(wkt.loads)

# SA2 polygons are stored in NZTM2000
sa2 = gpd.GeoDataFrame(
    sa2,
    geometry="geometry",
    crs="EPSG:2193"
)

# Convert SA2 polygons to same CRS as Airbnb coordinates
sa2 = sa2.to_crs("EPSG:4326")

# Match each Airbnb point to its SA2 polygon
airbnb = gpd.sjoin(
    airbnb,
    sa2[
        [
            "SA22019_V1_00",
            "SA22019_V1_00_NAME",
            "geometry"
        ]
    ],
    how="left",
    predicate="within"
)


# Rename columns
airbnb.rename(
    columns={
        "SA22019_V1_00": "sa2_code",
        "SA22019_V1_00_NAME": "sa2_name"
    },
    inplace=True
)


airbnb.to_csv(
        CLEANED_AIRBNB_SA2_FILE,
        index=False
    )

print("SA2_2019 codes assigned to airbnb listings successfully")