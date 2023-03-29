import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from .url_stringbuilder import getRightmoveRentString, updateIndex
from .utils import createOutputs, extractDate, formatPrice, getBeautifulSoupResponse, getDateUpdatedFromSoup, getDateUpdatedType, getImagesFromListing, loadBuffer, printNumberOfPagesScraped

def main():
    RIGHTMOVE_RENT_URL = getRightmoveRentString()

    # initialise index, this will keep track of the page numbers - 24 will be added to each iteration
    index = 0
    # Create an empty list to store the data for each listing
    data = []

    for pages in range(41):
        url = updateIndex(RIGHTMOVE_RENT_URL, index)
        soup = getBeautifulSoupResponse(url)
        listings = soup.find_all("div", class_="l-searchResult is-list")

        numberOfListings = int((soup.find("span", {"class": "searchHeader-resultCount"})).get_text().replace(",", ""))

        # Loop through each listing and extract the desired data
        for listing in listings:
            # Extract the property details
            details = listing.find("div", class_="propertyCard-details")
            address = details.find("address").get_text(strip=True)
            price_pcm = formatPrice(listing.find("span", class_="propertyCard-priceValue").get_text(strip=True), " pcm")
            price_pw = formatPrice(listing.find("span", class_="propertyCard-secondaryPriceValue").get_text(strip=True), " pw")
            description = details.find("h2", class_="propertyCard-title").get_text(strip=True)
            web_link = 'https://www.rightmove.co.uk%s' % (details.find("a", class_="propertyCard-link").get('href'))

            listing_response_soup = getBeautifulSoupResponse(web_link)
            date_updated = getDateUpdatedFromSoup(listing_response_soup)
            date_updated_type = getDateUpdatedType(date_updated)
            date_updated = extractDate(date_updated)

            images = []
            getImagesFromListing(listing_response_soup, images)

            # Add the data for this listing to the list
            data.append({"address": address, "price_pcm": price_pcm, "price_pw": price_pw, "date_updated": date_updated, "date_updated_type": date_updated_type, "description": description, "web_link": web_link, "images": images})

        printNumberOfPagesScraped(pages)
        loadBuffer()
        index += 24
        
        if index >= numberOfListings:
            break

    createOutputs(data, ['price_pcm', 'address'], 'rent')

if __name__ == "__main__":
    main()