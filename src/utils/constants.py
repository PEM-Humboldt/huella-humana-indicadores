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

# TODO: write description
CREATE_HF_INDICATORS_DESCRIPTION = """
Script description...
"""

# TODO: write description
CREATE_HF_PERSISTENCE_DESCRIPTION = """
Script description...
"""
