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

import fiona
import rasterio
from rasterio.features import shapes

from src.utils.constants import RECLASSIFICATION_VALUE_MAP
from src.utils.functions import reclassify_array

if __name__ == "__main__":

    # Change working directory to project's root
    os.chdir("..")

    output_folder = "data/shp/IHEH"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filepaths = glob.glob("data/tif/IHEH/*.tif")
    for filepath in filepaths:

        # Open raster and read first band as a NumPy array
        with rasterio.open(filepath) as src:

            arr = src.read(1)
            arr = reclassify_array(arr, RECLASSIFICATION_VALUE_MAP)

            basename = os.path.splitext(os.path.basename(filepath))[0]
            save_to = os.path.join(output_folder, f"{basename}.shp")
            driver = "ESRI Shapefile"
            schema = {"geometry": "Polygon", "properties": [("iheh", "int")]}
            kwargs = dict(driver=driver, crs=src.crs.to_wkt(), schema=schema)
            with fiona.open(save_to, "w", **kwargs) as dst:
                mask = arr != src.nodata
                features = shapes(arr, mask=mask, transform=src.transform)
                for feature in features:
                    record = {
                        "geometry": feature[0],
                        "properties": {"iheh": feature[1]}
                    }
                    dst.write(record)
