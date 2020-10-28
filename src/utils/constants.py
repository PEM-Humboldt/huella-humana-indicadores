# -----------------------------------------------------------------------
# Authors
# -------
# Marcelo Villa-Piñeros (mvilla@humboldt.org.co)
#
# Purpose
# -------
# Contains variables used to configure the behaviour of the main scripts.
# Every variable has an associated comment explaining its purpose.
# -----------------------------------------------------------------------

# Reclassification map to use in the reclassification of Human Footprint
# values. Each element of the list is a tuple with other two elements:
#   - tuple with the range of old values to replace.
#   - integer with the new value to replace old values with.
# The range of values is closed, meaning that both values are included
# when doing the reclassification.
RECLASSIFICATION_MAP = [
    ((0, 15), 0),
    ((16, 40), 1),
    ((41, 60), 2),
    ((60, 100), 3)
]

# Category map to convert reclassified values into categories. The keys
# must match the new values in RECLASSIFICATION MAP.
CATEGORY_MAP = {0: "natural", 1: "baja", 2: "media", 3: "alta"}

# Arbitrary value to assign to dynamic persistence categories (i.e. human
# footprint categories that change across time) before vectorizing the
# array. Must be different to new values in RECLASSIFICATION MAP.
PERSISTENCE_OTHER_VALUE = 4

# Category map to convert persistence values into categories. The keys,
# except for PERSISTENCE_OTHER_VALUE, must match the new values in
# RECLASSIFICATION MAP.
PERSISTENCE_CATEGORY_MAP = {
    0: "estable_natural",
    1: "estable_natural",
    2: "estable alta",
    3: "estable alta",
    PERSISTENCE_OTHER_VALUE: "dinamica"
}

# Arbitrary new NoData value for the intermediate persistence array.
# This value is not extracted from the original rasters as they can have
# different NoData values. This value is needeed to exclude NoData pixels
# from being vectorized.
PERSISTENCE_NODATA = 255

# Map of output field names. Values can be whatever field name the user
# wants in the output vector layers. Keys should not be changed.
HF_FIELD_NAMES = {
    "area": "area_ha",
    "average": "hf_avg",
    "category": "hf_cat",
    "persistence": "hf_pers",
    "protection": "binary_protected",
    "year": "hf_year"
}

# List of fields to use in the computation of the protection value.
PROTECTION_FIELDS = [
    "anu",
    "dcs",
    "dnmi",
    "drmi",
    "pnn",
    "pnr",
    "rfpn",
    "rfpr",
    "rn",
    "rnsc",
    "sfa",
    "sff",
    "sfl",
    "vp",
    "ar"
]

# Human Footprint fields to dissolve the indicators output vector layer.
# All the fields should come from HF_FIELD_NAMES and be accessed from the
# key rather than be an arbitrary value. For example, write
# HF_FIELD_NAMES.get("category") instead of "hf_cat".
HF_DISSOLVE_FIELDS = [
    HF_FIELD_NAMES.get("category"),
    HF_FIELD_NAMES.get("year"),
    HF_FIELD_NAMES.get("protection")
]

# Human Footprint fields to dissolve the persistence output vector layer.
# All the fields should come from HF_FIELD_NAMES and be accessed from the
# key rather than be an arbitrary value. For example, write
# HF_FIELD_NAMES.get("persistence") instead of "hf_pers".
PERSISTENCE_DISSOLVE_FIELDS = [HF_FIELD_NAMES.get("persistence")]

# Factor to multiply the resulting area of each polygon in the output
# vector layer by. This factor will be used only if the input data
# (geofences and rasters) have a projected coordinate reference system.
# Here are some useful factors:
# 1        -> square meters
# 0.0001   -> hectares
# 0.000001 -> square kilometers
AREA_FACTOR = 0.0001

# Tool description for the help message of create_hf_indicators.py.
CREATE_HF_INDICATORS_DESCRIPTION = """
Creates a geographic vector layer with the category, year and average of the human 
footprint by intersecting the original product with a specific geofences geographic 
vector layer.
"""

# Tool description for the help message of create_hf_persistence.py.
CREATE_HF_PERSISTENCE_DESCRIPTION = """
Creates a geographic vector layer with the persistence category of the human 
footprint across time by intersecting the original product with a specific geofences 
geographic vector layer.
"""

# output_path parameter description for the help message of both tools.
OUTPUT_PATH_HELP_TEXT = """
Relative or absolute path (including the extension) of the output file. If the folder
where the output file will be created does not exist, the folder is automatically 
created. Existing files will be overwritten. Example ./results/test/hf_indicators.shp
"""""

# geofences_path parameter description for the help message of both tools.
GEOFENCES_PATH_HELP_TEXT = """
Relative or absolute path of the input geofences file. Example: ./data/test/geofences.shp
"""

# rasters_path parameter description for the help message of both tools.
RASTERS_PATH_HELP_TEXT = """
Relative or absolute path of the folder containing the raster(s) of the original 
Human Footprint product. Rasters must be GeoTIFF files and their filenames must contain
(anywhere on the name) a four-digit sequence representing the year of the product (e.g.
IHEH_1970.tif). Example: ./data/test/IHEH
"""

# crs parameter description for the help message of both tools.
CRS_HELP_TEXT = """
Coordinate reference system to reproject the output layer to. Must be in the form 
epsg:{code}. For example: epsg:4326
"""
