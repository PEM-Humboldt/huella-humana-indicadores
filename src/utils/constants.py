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

HF_FIELD_NAMES = {
    "area": "area_ha",
    "average": "hf_avg",
    "category": "hf_cat",
    "protection": "binary_protected",
    "year": "hf_year",
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
    "ar",
]

HF_DISSOLVE_FIELDS = [
    HF_FIELD_NAMES.get("category"),
    HF_FIELD_NAMES.get("year"),
    HF_FIELD_NAMES.get("protected")
]

AREA_FACTOR = 0.0001

# TODO: write description
CREATE_HF_INDICATORS_DESCRIPTION = """
Script description...
"""
