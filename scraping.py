import requests
from bs4 import BeautifulSoup
import getting_data
# Scrape the webpage and find the URLs of the buttons you want to click
url = "https://www.earthenv.org/landcover"  # Replace with the actual URL
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

# Find the buttons or elements containing the URLs
button_elements = soup.find(id = "landcoverfull")  # Replace with the appropriate selector


td_elements = button_elements.find_all("td")
button_urls = []
for td in td_elements:
    link = td.find("a")
    if link:
        first_link = link["href"]
        button_urls.append(first_link)

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
    # Extract the filename from the URL or any other method
    
    # Save the file to disk
    with open(f"data/{filenames[idx]}", "wb") as file:
        file.write(file_response.content)

    

    print(f"File {filenames[idx]} downloaded and unzipped successfully.")

import pandas as pd
import numpy as np






df = pd.read_csv('data.csv')


df['keys'] = (keys := np.arange(len(df)))
values = []


coordinates = [(lat, lon) for lat, lon in df[["Latitude", "Longitude"]].to_records(index=False)]

for i in range(len(filenames)):
    name = f"data/{filenames[i]}"
    df = getting_data.grab(coordinates, df, name)

df.to_csv("final.csv", index=False)
