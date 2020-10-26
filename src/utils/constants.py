# -----------------------------------------------------------------------
#
# Authors
# -------
# Marcelo Villa-Piñeros (mvilla@humboldt.org.co)
# Jaime Burbano-Girón (jburbano@humboldt.org.co)
#
# Purpose
# -------
#
#
# -----------------------------------------------------------------------
RECLASSIFICATION_MAP = [((0, 15), 0), ((16, 40), 1), ((41, 60), 2), ((60, 100), 3)]

CATEGORY_MAP = {0: "natural", 1: "baja", 2: "media", 3: "alta"}

PERSISTENCE_OTHER_VALUE = 4
PERSISTENCE_CATEGORY_MAP = {
    0: "estable_natural",
    1: "estable_natural",
    2: "estable alta",
    3: "estable alta",
    PERSISTENCE_OTHER_VALUE: "dinamica"
}
PERSISTENCE_NODATA = 255

HF_FIELD_NAMES = {
    "area": "area_ha",
    "average": "hf_avg",
    "category": "hf_cat",
    "persistence": "hf_pers",
    "protection": "binary_protected",
    "year": "hf_year"
}

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

HF_DISSOLVE_FIELDS = [
    HF_FIELD_NAMES.get("category"),
    HF_FIELD_NAMES.get("year"),
    HF_FIELD_NAMES.get("protection")
]

PERSISTENCE_DISSOLVE_FIELDS = [HF_FIELD_NAMES.get("persistence")]

AREA_FACTOR = 0.0001


CREATE_HF_INDICATORS_DESCRIPTION = """
Creates a geographic vector layer with the category, year and average of the human 
footprint by intersecting the original product with a specific geofences geographic 
vector layer.
"""

# TODO: write description
CREATE_HF_PERSISTENCE_DESCRIPTION = """
Creates a geographic vector layer with the persistence category of the human 
footprint across time by intersecting the original product with a specific geofences 
geographic vector layer.
"""

OUTPUT_PATH_HELP_TEXT = """
Relative or absolute path (including the extension) of the output file. If the folder
where the output file will be created does not exist, the folder is automatically 
created. Existing files will be overwritten. Example ./results/test/hf_indicators.shp
"""""

GEOFENCES_PATH_HELP_TEXT = """
Relative or absolute path of the input geofences file. Example: ./data/test/geofences.shp
"""

RASTERS_PATH_HELP_TEXT = """
Relative or abolsute path of the folder containing the raster(s) of the original 
Human Footprint product. Rasters must be GeoTIFF files and their filenames must contain
(anywhere on the name) a four-digit sequence representing the year of the product (e.g.
IHEH_1970.tif). Example: ./data/test/IHEH
"""

CRS_HELP_TEXT = """
String with the EPSG code of the new coordinate reference system in the form epsg:code.
For example: epsg:4326
"""


