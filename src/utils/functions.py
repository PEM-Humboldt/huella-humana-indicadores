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
from typing import Generator

import geopandas
import numpy as np
import pandas as pd
from shapely.geometry import shape


def compute_protection_sequence(df: pd.DataFrame, fields: list) -> pd.Series:
    """

    Parameters
    ----------
    df:
    fields:

    Returns
    -------

    """
    # Validate that all fields passed are present in the DataFrame.
    assert all(field in df.columns for field in fields)

    binary_values = (df[fields] > 0).astype(int)
    return binary_values.apply(lambda x: "".join(x.values.astype(str)), axis=1)


def reclassify(arr: np.ndarray, value_map: list) -> np.ndarray:
    """
    Reclassifies an array by replacing values inside specified ranges
    with new values.

    Parameters
    ----------
    arr:       NumPy array to reclassify.
    value_map: List where each element is a tuple containing other two
               elements:

               - a tuple with a lower limit (from) and an upper limit
                 (to). The lower limit must be smaller than the upper
                 limit.
               - a specific value to reclassify the from-to range.

               The limits are closed, meaning that both the lower and
               upper limits are included in the range when doing the
               reclassification.

    Returns
    -------
    Reclassified NumPy array.

    Examples
    --------
    >>> arr = np.array([[5, 6, 2, 5], [8, 4, 3, 7], [6, 5, 4, 6], [8, 1, 1, 2]])
    >>> arr
    array([[5, 6, 2, 5],
           [8, 4, 3, 7],
           [6, 5, 4, 6],
           [8, 1, 1, 2]])
    >>> value_map = [((1, 4), 1), ((5, 9), 2)]
    >>> reclassify(arr, value_map)
    array([[2, 2, 1, 2],
           [2, 1, 1, 2],
           [2, 2, 1, 2],
           [2, 1, 1, 1]])
    """

    # Validate value_map input.
    assert isinstance(value_map, (list, tuple))
    for item in value_map:
        assert len(item) == 2
        assert len(item[0]) == 2
        assert isinstance(item[0][0], (float, int))
        assert isinstance(item[0][1], (float, int))
        assert isinstance(item[1], (float, int))
        assert item[0][0] < item[0][1]

    # In order to avoid overwriting already reclassified values, a copy
    # from the original array is created.
    new_arr = arr.copy()

    for item in value_map:
        lower = item[0][0]
        upper = item[0][1]
        value = item[1]
        mask = (arr >= lower) & (arr <= upper)
        new_arr = np.where(mask, value, new_arr)

    return new_arr


def shapes_to_geodataframe(
        features: Generator, crs: str, field_name: str = "value"
) -> geopandas.GeoDataFrame:
    """

    Parameters
    ----------
    features:   generator returned by the rasterio.features.shapes
                function.
    crs:        well-known text of a coordinate reference system.
    field_name: name of the column to store the raster's original pixel
                value.

    Returns
    -------
    Tuple with:
        - GeoDataFrame with all the features and their respective
        values.
        - Field name.
    """
    # Create empty dictionary to store the features geometries and
    # values.
    results = {field_name: [], "geometry": []}

    for i, feature in enumerate(features):
        results["geometry"].append(shape(feature[0]))
        results[field_name].append(feature[1])

    return geopandas.GeoDataFrame(results, crs=crs), field_name
