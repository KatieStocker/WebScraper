import requests, json, re
from bs4 import BeautifulSoup
import pandas as pd
import os
from .url_stringbuilder import getRightmoveBuyString, updateIndex

def main():
    RIGHTMOVE_BUY_URL = getRightmoveBuyString()

    # initialise index, this will keep track of the page numbers - 24 will be added to each iteration
    index = 0
    # Create an empty list to store the data for each listing
    data = []

    for pages in range(41):
        url = updateIndex(RIGHTMOVE_BUY_URL, index)

        # Send a GET request to the URL and get the response object
        response = requests.get(url)

        # Parse the response object with BeautifulSoup and extract the property listings
        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", class_="l-searchResult is-list")
        numberOfListings = int((soup.find("span", {"class": "searchHeader-resultCount"})).get_text().replace(",", ""))

        # Loop through each listing and extract the desired data
        for listing in listings:
            # Extract the property details
            details = listing.find("div", class_="propertyCard-details")
            address = details.find("address").get_text(strip=True)
            price = listing.find("div", class_="propertyCard-priceValue").get_text(strip=True)
            description = (details.find("a", class_="propertyCard-link").get_text(strip=True)).replace('for sale', 'for sale, ')
            web_link = 'https://www.rightmove.co.uk%s' % (details.find("a", class_="propertyCard-link").get('href'))
            # Extract the property features, such as number of bedrooms and type
            features = (details.find("h2", class_="propertyCard-title").get_text(strip=True)).replace(' for sale', '')

            listing_info = listing.find("div", class_="propertyCard-headerLabel")
            extra_info = ""

            if listing_info:
                if listing_info.get_text(strip=True) == "Premium Listing":
                    extra_info = ""
                else:
                    extra_info = listing_info.get_text(strip=True)

            # Add the data for this listing to the list
            data.append({"address": address, "price": price, "description": description, "features": features, "web_link": web_link, "extra_info": extra_info})

        print(f"You have scraped through {pages + 1} pages")
        
        index += 24
        
        if index >= numberOfListings:
            break

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    # Sort by price and address, drop any duplicate entries, and save to a CSV file
    df.sort_values(['price', 'address']).drop_duplicates('web_link', keep='last').to_csv("Output/rightmove_properties_buy.csv", index=False, sep='|')

if __name__ == "__main__":
    main()