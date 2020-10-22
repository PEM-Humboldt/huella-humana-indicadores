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
import argparse
import glob
import os
import warnings

import geopandas
import numpy as np
import rasterio
from rasterio.features import shapes

from src.utils.constants import RECLASSIFICATION_MAP, CREATE_HF_PERSISTENCE_DESCRIPTION
from src.utils.functions import (
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
    nodata: int,
    hf_field_names: dict,
    protection_fields: list,
    hf_dissolve_fields: list,
    area_factor: float,
    output_crs: str = None
) -> None:

    # Grab output folder from output path and create the folder
    # if it does not exist already.
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    geofences = geopandas.read_file(geofences_path)
    result = geopandas.GeoDataFrame()

    raster_filenames = sorted(glob.glob(os.path.join(rasters_path, "*.tif")))
    stack = []
    for raster_fn in raster_filenames:
        src = rasterio.open(raster_fn)
        arr = src.read(1)
        arr = reclassify(arr, reclassification_map)
        arr = np.ma.array(arr, mask=(arr == src.nodata))
        stack.append(arr)
    stack = np.ma.stack(stack)

    equal_values = np.all(stack == stack[0, ...], axis=0)
    arr = np.ma.where(equal_values, stack[0, ...], other_value)
    arr = stack.filled(nodata)

    mask = arr != nodata
    features = shapes(arr, mask=mask, connectivity=8, transform=src.transform)
    features, value_field = shapes_to_geodataframe(features, src.crs.to_string())

    result = geopandas.overlay(geofences, features, how="intersection")

    # Assign human foot print persistence categories based on the
    # reclassified values.
    categories = result[value_field].map(category_map)
    result[hf_field_names.get("category")] = categories

    protection_sequences = compute_protection_sequence(result, protection_fields)
    result[hf_field_names.get("protection")] = protection_sequences

    # TODO: document these steps.
    dissolve_fields = list(geofences.columns) + hf_dissolve_fields
    dissolve_fields.remove("geometry")
    if None in dissolve_fields:
        dissolve_fields.remove(None)
    result = result.dissolve(by=dissolve_fields, aggfunc="mean")
    result = result.reset_index()

    # Remove unused fields
    result = result.drop(protection_fields + [value_field], axis=1)

    # Compute area only if hte coordinate reference system is projected.
    if result.crs.is_projected:
        result[hf_field_names.get("area")] = result.geometry.area * area_factor
    else:
        warnings.warn("Area was not computed because input data is not projected.")

    # Reproject file if and output coordinate reference system was
    # specified.
    if output_crs:
        result = result.to_crs(output_crs)

    result.to_file(output_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=CREATE_HF_PERSISTENCE_DESCRIPTION)
