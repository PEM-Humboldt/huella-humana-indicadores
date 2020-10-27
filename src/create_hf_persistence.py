# -----------------------------------------------------------------------
# Authors
# -------
# Marcelo Villa-Piñeros (mvilla@humboldt.org.co)
# Jaime Burbano-Girón (jburbano@humboldt.org.co)
#
# Purpose
# -------
# Creates a geographic vector layer with the Human Footprint persistence
# category across time. The layer is created by computing the pixel-wise
# persistence across all Human Footprint products (i.e. all years) and
# intersecting the vectorized persistence categories with a specific
# geofences layer. This script has a command line-like interface and
# it is supposed to be executed from a terminal by passing a series of
# positional arguments. To execute the script, open a terminal and run
# the following command:
# python create_hf_persistence.py -h.
# This will display a help message with the usage of the script and the
# description of the parameters.
# -----------------------------------------------------------------------
import argparse
import glob
import os
import warnings

import geopandas
import numpy as np
import rasterio
from rasterio.features import shapes

from utils.constants import (
    RECLASSIFICATION_MAP,
    CREATE_HF_PERSISTENCE_DESCRIPTION,
    PERSISTENCE_OTHER_VALUE,
    PERSISTENCE_CATEGORY_MAP,
    PERSISTENCE_NODATA,
    HF_FIELD_NAMES,
    PROTECTION_FIELDS,
    PERSISTENCE_DISSOLVE_FIELDS,
    AREA_FACTOR,
    OUTPUT_PATH_HELP_TEXT,
    GEOFENCES_PATH_HELP_TEXT,
    RASTERS_PATH_HELP_TEXT,
    CRS_HELP_TEXT
)
from utils.functions import (
    reclassify,
    shapes_to_geodataframe,
    compute_protection_sequence
)


def main(
    output_path: str,
    geofences_path: str,
    rasters_path: str,
    reclassification_map: list,
    other_value: int,
    category_map: dict,
    new_nodata: int,
    hf_field_names: dict,
    protection_fields: list,
    hf_dissolve_fields: list,
    area_factor: float,
    output_crs: str = None,
) -> None:

    # Grab output folder from output path and create the folder
    # if it does not exist already.
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    geofences = geopandas.read_file(geofences_path)

    # Create a 3D NumPy array with all the reclassified Human Footprint
    # rasters. Each band is masked with its respective NoData value in
    # order to ignore NoData pixels in the persistence computation.
    raster_filenames = sorted(glob.glob(os.path.join(rasters_path, "*.tif")))
    stack = []
    for raster_fn in raster_filenames:
        src = rasterio.open(raster_fn)
        arr = src.read(1)
        arr = reclassify(arr, reclassification_map)
        arr = np.ma.array(arr, mask=(arr == src.nodata))
        stack.append(arr)
    stack = np.ma.stack(stack)

    # Leave all the pixels that remain equal across time as they are but
    # assign a new value to pixels where values change. This converts a
    # 3D array back into a 2D array.
    equal_values = np.all(stack == stack[0, ...], axis=0)
    arr = np.ma.where(equal_values, stack[0, ...], other_value)

    # Assign a new arbitrary NoData value to the masked pixels.
    arr = arr.filled(new_nodata)

    # Vectorize the resulting array and convert all the features to a
    # GeoDataFrame. A mask for non-NoData values must be passed to the
    # shapes function in order to avoid vectorization of those values.
    mask = arr != new_nodata
    features = shapes(arr, mask=mask, connectivity=8, transform=src.transform)
    features, value_field = shapes_to_geodataframe(features, src.crs.to_string())

    result = geopandas.overlay(geofences, features, how="intersection")

    # Assign human foot print persistence categories based on the
    # reclassified values.
    categories = result[value_field].map(category_map)
    result[hf_field_names.get("persistence")] = categories

    protection_sequences = compute_protection_sequence(result, protection_fields)
    result[hf_field_names.get("protection")] = protection_sequences

    # Get a list of all the dissolve fields and use them to dissolve
    # the GeoDataFrame. Index must be reset to keep fields used as fields
    # and not as index.
    dissolve_fields = list(geofences.columns) + hf_dissolve_fields
    dissolve_fields.remove("geometry")
    if None in dissolve_fields:
        dissolve_fields.remove(None)
    result = result.dissolve(by=dissolve_fields, aggfunc="mean")
    result = result.reset_index()

    # Remove unused fields
    result = result.drop(protection_fields + [value_field], axis=1)

    # Compute area only if the coordinate reference system is projected.
    if result.crs.is_projected:
        result[hf_field_names.get("area")] = result.geometry.area * area_factor
    else:
        warnings.warn("Area was not computed because input data is not projected.")

    # Reproject file if an output coordinate reference system was
    # specified.
    if output_crs:
        result = result.to_crs(output_crs)

    result.to_file(output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=CREATE_HF_PERSISTENCE_DESCRIPTION)
    parser.add_argument("output_path", type=str, help=OUTPUT_PATH_HELP_TEXT)
    parser.add_argument("geofences_path", type=str, help=GEOFENCES_PATH_HELP_TEXT)
    parser.add_argument("rasters_path", type=str, help=RASTERS_PATH_HELP_TEXT)
    parser.add_argument("-crs", type=str, help=CRS_HELP_TEXT)
    args = parser.parse_args()

    main(
        args.output_path,
        args.geofences_path,
        args.rasters_path,
        RECLASSIFICATION_MAP,
        PERSISTENCE_OTHER_VALUE,
        PERSISTENCE_CATEGORY_MAP,
        PERSISTENCE_NODATA,
        HF_FIELD_NAMES,
        PROTECTION_FIELDS,
        PERSISTENCE_DISSOLVE_FIELDS,
        AREA_FACTOR,
        output_crs=args.crs
    )
