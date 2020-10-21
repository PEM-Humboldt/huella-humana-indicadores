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
import re
import warnings

import geopandas
import rasterio
from rasterio.features import shapes
from rasterstats import zonal_stats

from src.utils.constants import (
    CREATE_HF_INDICATORS_DESCRIPTION,
    RECLASSIFICATION_MAP,
    HF_FIELD_NAMES,
    CATEGORY_MAP,
    PROTECTION_FIELDS,
    HF_DISSOLVE_FIELDS,
    AREA_FACTOR
)
from src.utils.functions import (
    reclassify,
    shapes_to_geodataframe,
    compute_protection_sequence,
)


def main(
    output_path: str,
    geofences_path: str,
    rasters_path: str,
    reclassification_map: list,
    hf_field_names: dict,
    category_map: dict,
    protection_fields: list,
    hf_dissolve_fields: list,
    area_factor: float = 1.0,
    output_crs: str = None,
) -> None:
    """

    Parameters
    ----------
    output_path
    geofences_path
    rasters_path
    reclassification_map
    hf_field_names
    category_map
    protection_fields
    hf_dissolve_fields
    area_factor
    output_crs

    Returns
    -------
    None
    """

    # Grab output folder from output path and create the folder
    # if it does not exist already.
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    geofences = geopandas.read_file(geofences_path)
    result = geopandas.GeoDataFrame()

    raster_filenames = sorted(glob.glob(os.path.join(rasters_path, "*.tif")))
    for raster_fn in raster_filenames:

        # Open raster and read it's first (and only) band. Then,
        # reclassify those values.
        src = rasterio.open(raster_fn)
        arr = src.read(1)
        arr = reclassify(arr, reclassification_map)

        # Vectorize the reclassified raster and convert all the features
        # to a GeoDataFrame. A mask specifying non-NoData values must be
        # passed to the shapes function in order to avoid vectorizing
        # those values.
        mask = arr != src.nodata
        features = shapes(arr, mask=mask, connectivity=8, transform=src.transform)
        features, value_field = shapes_to_geodataframe(features, src.crs.to_string())

        intersection = geopandas.overlay(geofences, features, how="intersection")

        # Assign human foot print categories based on the reclassified
        # values.
        categories = intersection[value_field].map(category_map)
        intersection[hf_field_names.get("category")] = categories

        # Compute human footprint average using zonal statistics.
        means = [item.get("mean") for item in zonal_stats(intersection, raster_fn)]
        intersection[hf_field_names.get("average")] = means

        # Get human foot print year using a regular expression. The
        # regular expression captures the first four digit number
        # that is between a reasonable range (1900 - 2099). The
        # expression was taken from:
        # https://stackoverflow.com/a/49853325/7144368
        year = re.findall(r"(?:19|20)\d{2}", raster_fn)[0]
        intersection[hf_field_names.get("year")] = year

        result = result.append(intersection, ignore_index=True)

    protection_sequences = compute_protection_sequence(result, protection_fields)
    result[hf_field_names.get("protection")] = protection_sequences

    # TODO: document these steps.
    dissolve_fields = list(geofences.columns) + hf_dissolve_fields
    dissolve_fields.remove("geometry")
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

    parser = argparse.ArgumentParser(description=CREATE_HF_INDICATORS_DESCRIPTION)
    parser.add_argument("output_path", type=str, help="Path of the output file.")
    parser.add_argument("geofences_path", type=str, help="Path of the geofences file.")
    parser.add_argument("rasters_path", type=str, help="Path of the raster files.")
    parser.add_argument(
        "-crs", type=str, help="EPSG code of the new coordinate reference system"
    )
    args = parser.parse_args()

    main(
        args.output_path,
        args.geofences_path,
        args.rasters_path,
        RECLASSIFICATION_MAP,
        HF_FIELD_NAMES,
        CATEGORY_MAP,
        PROTECTION_FIELDS,
        HF_DISSOLVE_FIELDS,
        area_factor=AREA_FACTOR,
        output_crs=args.crs,
    )
