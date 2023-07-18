#imports
import rasterio
import pandas as pd
import numpy as np

#function that we will call from the main script
def grab(coordinates, df, filename):

    #we are going to open the file
    #then get information about the tif file and get the band that has the data on it
    #then for all of the coordinates, we will transform the latitude and longitude to the width and height of the file
    #then we use those numbers to find the value we are looking for and append it to the values list
    #finally we save it to a dictionary and map it back to the dataframe
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



