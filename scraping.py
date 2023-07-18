#imports
import requests
from bs4 import BeautifulSoup
import getting_data
import pandas as pd
import numpy as np

#get the webpage
url = "https://www.earthenv.org/landcover"  
response = requests.get(url)

#get the html of the webpage
soup = BeautifulSoup(response.content, "html.parser")

#select the table with the downloads we need
table = soup.find(id = "landcoverfull")  

#get every row 
td_elements = table.find_all("td")

#urls of all downloads
button_urls = []

#go through each row and save the download link to the button_urls list
for td in td_elements:
    link = td.find("a")
    if link:
        first_link = link["href"]
        button_urls.append(first_link)

#filenames list used for filenames
filenames = [
    "Evergreen_Deciduous_Needleleaf_Trees.tif",
    "Evergreen_Broadleaf_Trees.tif",
    "Deciduous_Broadleaf_Trees.tif",
    "Mixed_Other_Trees.tif",
    "Shrubs.tif",
    "Herbaceous_Vegetation.tif",
    "Cultivated_and_Managed_Vegetation.tif",
    "Regularly_Flooded_Vegetation.tif",
    "Urban_Built-up.tif",
    "Snow_Ice.tif",
    "Barren.tif",
    "Open_Water.tif"
]



for idx, button_url in enumerate(button_urls):
    # Download the file
    file_response = requests.get(button_url)
    
    
    # Save the file to data directory
    with open(f"data/{filenames[idx]}", "wb") as file:
        file.write(file_response.content)

    

    print(f"File {filenames[idx]} downloaded and unzipped successfully.")


###


#read in data
df = pd.read_csv('data.csv')

#create keys variable and column in dataframe
#we will use this to map the data together
df['keys'] = (keys := np.arange(len(df)))
values = []

#now we create a list of tuples with latitude and longitude that we can use
#these tuples will be how we access the data from the tif file
coordinates = [(lat, lon) for lat, lon in df[["Latitude", "Longitude"]].to_records(index=False)]


for i in range(len(filenames)):
    name = f"data/{filenames[i]}"

    #now we go into the getting data module to get the data from the tif file
    df = getting_data.grab(coordinates, df, name)

df.to_csv("final.csv", index=False)
