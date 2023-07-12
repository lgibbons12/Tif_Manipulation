import rasterio
from rasterio.transform import from_origin
import pandas as pd
import numpy as np
def grab(coordinates, df, filename):
    with rasterio.open(filename) as src:
        values = []
        keys = np.arange(len(df))
        #data from tif
        
        width = src.width
        height = src.height

        
        
        band = src.read(1)

        for lat, lon in coordinates:
            row, col = rasterio.transform.rowcol(src.transform, xs = lon, ys = lat)
            if 0 <= row < height and 0 <= col < width:
                value = band[row, col]
                values.append(value)
            else:
                values.append(None)

        

    dict = pd.DataFrame({"keys": keys, "Values": values}).set_index("keys")["Values"].to_dict()

    df[filename] = df["keys"].map(dict)

    return df



