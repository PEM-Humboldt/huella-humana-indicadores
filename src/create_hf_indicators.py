# -----------------------------------------------------------------------
# Authors
# -------
# Marcelo Villa-Piñeros (mvilla@humboldt.org.co)
# Jaime Burbano-Girón (jburbano@humboldt.org.co)
#
# Purpose
# -------
# Creates a geographic vector layer with the Human Footprint year,
# category and average. The layer is created by intersecting the
# vectorized Human Footprint rasters with a specific geofences layer.
# This script has a command line-like interface and it is supposed to be
# executed from a terminal by passing a series of positional arguments.
# To execute the script, open a terminal and run the following command:
# python create_hf_indicators.py -h.
# This will display a help message with the usage of the script and the
# description of the parameters.
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

from utils.constants import (
    CREATE_HF_INDICATORS_DESCRIPTION,
    RECLASSIFICATION_MAP,
    HF_FIELD_NAMES,
    CATEGORY_MAP,
    PROTECTION_FIELDS,
    HF_DISSOLVE_FIELDS,
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
    hf_field_names: dict,
    category_map: dict,
    protection_fields: list,
    hf_dissolve_fields: list,
    area_factor: float = 1.0,
    output_crs: str = None
) -> None:
    """
    Creates a geographic vector layer resulting from the intersection
    of vectorized Human Footprint categories and a specific layer of
    geofences. Human Footprint categories are vectorized and intersected
    for each individual Human Footprint product (each individual product
    corresponds to a unique year). The output layer contains three fields
    related to the Human Footprint product: (1) category, (2) year and
    (3) average. The first two result from the intersection between the
    vectorized categories and the geofences. The third one is computed
    using zonal statistics. Furthermore, protection-related fields from
    the geofences are used to compute a protection-level field in the
    output layer. The output layer is dissolved by a configurable list of
    fields and is optionally reprojected to a specified coordinate
    reference system.

    Parameters
    ----------
    output_path:          Relative or absolute path (including the
                          extension) of the output file.
    geofences_path:       Relative or absolute path of the input
                          geofences file.
    rasters_path:         Relative or absolute path of the folder
                          containing the raster(s) of the original Human
                          Footprint product.
    reclassification_map: List of ranges of old values and their
                          corresponding new values to reclassify a NumPy
                          array.
    hf_field_names:       Dictionary containing user defined names for
                          the output fields.
    category_map:         Category names for each of the new values in
                          reclassification_map.
    protection_fields:    Fields to be used in the computation of the
                          output protection field.
    hf_dissolve_fields:   Human Footprint-related fields to use in the
                          dissolve process of the output layer.
    area_factor:          Factor to multiply the resulting area by.
                          Useful to convert meters to other units (e.g.
                          hectares).
    output_crs:           Coordinate reference system to reproject the
                          output layer to. Must be in the form
                          epsg:{code}.

    Returns
    -------
    None

    Notes
    -----
    Input Human Footprint products and geofences layer must share the
    same coordinate reference system. Otherwise, the intersection between
    them will fail.

    Area will only be computed if the coordinate reference system of the
    input files is projected. The reason behind this is to avoid area
    computations in non-planar units (e.g. degrees).
    """

    # Grab output folder from output path and create the folder
    # if it does not exist already.
    output_folder = os.path.dirname(output_path)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    geofences = geopandas.read_file(geofences_path)

    # Create empty GeoDataFrame to store the result.
    result = geopandas.GeoDataFrame()

    raster_filenames = sorted(glob.glob(os.path.join(rasters_path, "*.tif")))
    for raster_fn in raster_filenames:

        # Open raster and read it's first (and only) band. Then,
        # reclassify those values.
        src = rasterio.open(raster_fn)
        arr = src.read(1)
        arr = reclassify(arr, reclassification_map)

        # Vectorize the reclassified raster and convert all the features
        # to a GeoDataFrame. A mask for non-NoData values must be passed
        # to the shapes function in order to avoid vectorization of those
        # values.
        mask = arr != src.nodata
        features = shapes(arr, mask=mask, connectivity=8, transform=src.transform)
        features = shapes_to_geodataframe(features, src.crs.to_string())
        value_field = features.columns[0]

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

    # Get a list of all the dissolve fields and use them to dissolve
    # the GeoDataFrame. Index must be reset to keep fields used as fields
    # and not as index.
    dissolve_fields = list(geofences.columns) + hf_dissolve_fields
    dissolve_fields.remove("geometry")
    if None in dissolve_fields:
        dissolve_fields.remove(None)
    result = result.dissolve(by=dissolve_fields, aggfunc="mean")
    result = result.reset_index()

    # Remove unused fields.
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

    parser = argparse.ArgumentParser(description=CREATE_HF_INDICATORS_DESCRIPTION)
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
        HF_FIELD_NAMES,
        CATEGORY_MAP,
        PROTECTION_FIELDS,
        HF_DISSOLVE_FIELDS,
        area_factor=AREA_FACTOR,
        output_crs=args.crs
    )
