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
import numpy as np


def reclassify_array(arr: np.ndarray, value_map: list) -> np.ndarray:
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
    >>> reclassify_array(arr, value_map)
    array([[2, 2, 1, 2],
           [2, 1, 1, 2],
           [2, 2, 1, 2],
           [2, 1, 1, 1]])
    """
    # Validate value_map input
    for item in value_map:
        assert (len(item) == 2)
        assert (len(item[0]) == 2)
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