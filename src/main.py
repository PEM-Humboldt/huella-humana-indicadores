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
import glob
import os
import re

import geopandas
import rasterio
from rasterio.features import shapes
from rasterstats import zonal_stats

from src.utils.constants import (
    RECLASSIFICATION_MAP,
    CATEGORY_MAP,
    HF_FIELD_NAMES,
    PROTECTION_FIELDS,
    HF_DISSOLVE_FIELDS,
    AREA_FACTOR
)
from src.utils.functions import (
    reclassify_array,
    shapes_to_geodataframe,
    compute_protection
)
from src.utils.paths import OUTPUT_FOLDER, GEOFENCES_PATH, IHEH_PATH, BIOMES_PATH

if __name__ == "__main__":

    # Change working directory to project's root
    os.chdir("..")

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    geofences = geopandas.read_file(GEOFENCES_PATH)
    geofences = geofences.to_crs("epsg:3116")

    result = geopandas.GeoDataFrame()

    raster_filenames = sorted(glob.glob(os.path.join(IHEH_PATH, "*.tif")))
    raster_fn = raster_filenames[1]  # Grab the test file

    for raster_fn in raster_filenames:

        src = rasterio.open(raster_fn)

        arr = src.read(1)
        arr = reclassify_array(arr, RECLASSIFICATION_MAP)
        mask = arr != src.nodata

        features = shapes(arr, mask=mask, connectivity=8, transform=src.transform)
        hf_features, value_field = shapes_to_geodataframe(features, src.crs.to_string())

        intersection = geopandas.overlay(geofences, hf_features, how="intersection")

        # Assign human foot print categories based on the reclassified
        # values.
        intersection[HF_FIELD_NAMES.get("category")] = intersection[value_field].map(
            CATEGORY_MAP
        )

        # Compute human footprint average using zonal statistics.
        stats = zonal_stats(intersection, raster_fn)
        intersection[HF_FIELD_NAMES.get("average")] = [item.get("mean") for item in stats]

        # Get human foot print year using a regular expression. The
        # regular expression captures the first four digit number
        # that is between a reasonable range (1900 - 2099). The
        # expression was taken from:
        # https://stackoverflow.com/a/49853325/7144368
        year = re.findall(r"(?:19|20)\d{2}", raster_fn)[0]
        intersection[HF_FIELD_NAMES.get("year")] = year

        result = result.append(intersection, ignore_index=True)

    result[HF_FIELD_NAMES.get("protection")] = compute_protection(result, PROTECTION_FIELDS)

    result = result.drop("value", axis=1)

    dissolve_fields = list(geofences.columns) + HF_DISSOLVE_FIELDS
    dissolve_fields.remove("geometry")
    result = result.dissolve(by=dissolve_fields, aggfunc="mean")
    result = result.reset_index()

    # TODO intersect with strategic ecosystems
    for biome_fn in glob.glob(os.path.join(BIOMES_PATH, "*.shp")):
        pass

    # Compute area in hectares.
    result["area_ha"] = result.geometry.area * AREA_FACTOR

    # TODO reproject
    pass
