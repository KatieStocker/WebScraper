import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from .url_stringbuilder import getRightmoveRentString, updateIndex
from .utils import extractDate, formatDateAvailable, formatLettingDetailTitle, formatLettingDetailValue, getBeautifulSoupResponse, getDateUpdatedFromSoup, getDateUpdatedType, getImagesFromListing
from global_utils import createOutputs, formatPrice, loadBuffer, printNumberOfPagesScraped

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

            letting_details_list = []
            getLettingDetails(listing_response_soup, letting_details_list)

            property_type = listing_response_soup.find("div", class_="_3ZGPwl2N1mHAJH3cbltyWn").find("div", class_="_3OGW_s5TH6aUqi4uHum5Gy").text

            # Add the data for this listing to the list
            data.append({"address": address, "price_pcm": price_pcm, "price_pw": price_pw, "date_updated": date_updated, "date_updated_type": date_updated_type, "description": description, "property_type": property_type, "letting_details": letting_details_list, "web_link": web_link, "images": images})

        printNumberOfPagesScraped(pages)
        loadBuffer()
        index += 24
        
        if index >= numberOfListings:
            break

    createOutputs(data, ['price_pcm', 'address'], 'rent', 'rightmove')

def getLettingDetails(soup, detail_list):
    letting_details = soup.find_all("div", class_="_2RnXSVJcWbWv4IpBC1Sng6")

    for letting_detail in letting_details:
        dt_string = letting_detail.find("dt").text.replace(": ", "")
        dd_string = letting_detail.find("dd").text.replace("A deposit provides security for a landlord against damage, or unpaid rent by a tenant.Read more about deposit in our glossary page.", "")

        dd_string = formatDateAvailable(dt_string, dd_string)
        dd_string = formatLettingDetailValue(dd_string)
        dt_string = formatLettingDetailTitle(dt_string)

        detail_list.append({dt_string: dd_string})

if __name__ == "__main__":
    main()