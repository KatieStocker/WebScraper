import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

RIGHTMOVE_RENT_URL = os.getenv('RIGHTMOVE_RENT_URL')

# Send a GET request to the URL and get the response object
response = requests.get(RIGHTMOVE_RENT_URL)

# Parse the response object with BeautifulSoup and extract the property listings
soup = BeautifulSoup(response.content, "html.parser")
listings = soup.find_all("div", class_="l-searchResult is-list")

# Create an empty list to store the data for each listing
data = []

# Loop through each listing and extract the desired data
for listing in listings:
    # Extract the property details
    details = listing.find("div", class_="propertyCard-details")
    address = details.find("address").get_text(strip=True)
    price_pcm = listing.find("span", class_="propertyCard-priceValue").get_text(strip=True)
    price_pw = listing.find("span", class_="propertyCard-secondaryPriceValue").get_text(strip=True)
    description = (details.find("a", class_="propertyCard-link").get_text(strip=True)).replace('for sale', 'for sale, ')
    web_link = 'https://www.rightmove.co.uk%s' % (details.find("a", class_="propertyCard-link").get('href'))
    # Extract the property features, such as number of bedrooms and type
    features = str((details.find("h2", class_="propertyCard-title").get_text(strip=True)).replace(' for sale', ''))

    # Add the data for this listing to the list
    data.append({"address": address, "price pcm": price_pcm, "price_pw": price_pw, "description": description, "features": features, "web_link": web_link})

# Convert the data to a pandas DataFrame and save it to a CSV file
df = pd.DataFrame(data)
df.to_csv("rightmove_properties_rent.csv", index=False)