import requests, json, re
from bs4 import BeautifulSoup
import pandas as pd
import os
from .url_stringbuilder import getRightmoveBuyString, updateIndex
import time
from datetime import date, timedelta
import random

def main():
    RIGHTMOVE_BUY_URL = getRightmoveBuyString()

    # initialise index, this will keep track of the page numbers - 24 will be added to each iteration
    index = 0
    # Create an empty list to store the data for each listing
    data = []

    for pages in range(41):
        url = updateIndex(RIGHTMOVE_BUY_URL, index)
        soup = getBeautifulSoupResponse(url)
        
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
            features = (details.find("h2", class_="propertyCard-title").get_text(strip=True)).replace(' for sale', '')

            listing_info = listing.find("div", class_="propertyCard-headerLabel")
            extra_info = getExtraInfoFromListing(listing_info)

            listing_response_soup = getBeautifulSoupResponse(web_link)
            date_updated = getDateUpdated(listing_response_soup.find('div', class_='_2nk2x6QhNB1UrxdI5KpvaF'))
            date_updated_type = getDateUpdatedType(date_updated)
            date_updated = extractDate(date_updated)
            tenure = getTenure(listing_response_soup)

            # Add the data for this listing to the list
            data.append({"address": address, "price": price, "tenure": tenure, "date_updated": date_updated, "date_updated_type": date_updated_type, "description": description, "features": features, "web_link": web_link, "extra_info": extra_info})

        printNumberOfPagesScraped(pages)
        # code to ensure that we do not overwhelm the website
        time.sleep(random.randint(1, 3))

        index += 24
        
        if index >= numberOfListings:
            break
            
    createOutputs(data)


def createOutputs(data):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    print("Creating output files...")
    # Sort by price and address, drop any duplicate entries, and save to a CSV file
    df.sort_values(['price', 'address']).drop_duplicates('web_link', keep='last').to_csv("Output/rightmove_properties_buy.csv", index=False, sep='|')
    # Sort by price and address, drop any duplicate entries, and save to a JSON file
    df.sort_values(['price', 'address']).drop_duplicates('web_link', keep='last').to_json("Output/rightmove_properties_buy.json", orient='records')
    print("Outputs have been created.")

def extractDate(date_updated):
    return date_updated.replace("Added on ", "").replace("Added ", "").replace("Reduced on ", "").replace("Reduced ", "")

def getBeautifulSoupResponse(url):
    # Send a GET request to the URL and get the response object
    response = requests.get(url)
    # Parse the response object with BeautifulSoup and extract
    return BeautifulSoup(response.content, "html.parser")

def getDateUpdated(date_updated):
    if date_updated:
        date_updated = date_updated.get_text(strip=True)
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)

        if "today" in date_updated:
            date_updated = date_updated.replace("today", today_date.strftime("%d/%m/%Y"))

        if "yesterday" in date_updated:
            date_updated = date_updated.replace("yesterday", yesterday_date.strftime("%d/%m/%Y"))
    else:
        date_updated = ""

    return date_updated

def getDateUpdatedType(date_updated):
    date_updated_type = "Added"
    if date_updated:
        if "Reduced" in date_updated:
            date_updated_type = "Reduced"
    else:
        date_updated_type = ""

    return date_updated_type

def getExtraInfoFromListing(listing_info):
    extra_info = ""
    if listing_info:
        if listing_info.get_text(strip=True) != "Premium Listing":
            extra_info = listing_info.get_text(strip=True)
    return extra_info

def getTenure(response):
    property_details = response.find('div', class_='_4hBezflLdgDMdFtURKTWh')
    return property_details.find('div', class_='_32IXcntQDSML3xVUkSdyXN').find('div', class_='_3ZGPwl2N1mHAJH3cbltyWn').get_text(strip=True) if property_details.find('div', class_='_32IXcntQDSML3xVUkSdyXN') else ""

def printNumberOfPagesScraped(pages):
    numberOfPages = pages + 1
    print(f"You have scraped through {numberOfPages} {'page' if numberOfPages == 1 else 'pages'}")


if __name__ == "__main__":
    main()