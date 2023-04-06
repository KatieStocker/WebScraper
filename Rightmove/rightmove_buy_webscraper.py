import os
from .url_stringbuilder import getRightmoveBuyString, updateIndex
from .utils import extractDate, getBeautifulSoupResponse, getDateUpdatedFromSoup, getDateUpdatedType, getImagesFromListing, loadBuffer, printNumberOfPagesScraped
from global_utils import createOutputs, formatPrice

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
            price = formatPrice(listing.find("div", class_="propertyCard-priceValue").get_text(strip=True), "")
            description = (details.find("a", class_="propertyCard-link").get_text(strip=True)).replace('for sale', 'for sale, ')
            web_link = 'https://www.rightmove.co.uk%s' % (details.find("a", class_="propertyCard-link").get('href'))
            features = (details.find("h2", class_="propertyCard-title").get_text(strip=True)).replace(' for sale', '')

            listing_info = listing.find("div", class_="propertyCard-headerLabel")
            extra_info = getExtraInfoFromListing(listing_info)

            listing_response_soup = getBeautifulSoupResponse(web_link)
            date_updated = getDateUpdatedFromSoup(listing_response_soup)
            date_updated_type = getDateUpdatedType(date_updated)
            date_updated = extractDate(date_updated)
            tenure = getTenure(listing_response_soup)
            
            images = []
            getImagesFromListing(listing_response_soup, images)

            # Add the data for this listing to the list
            data.append({"address": address, "price": price, "tenure": tenure, "date_updated": date_updated, "date_updated_type": date_updated_type, "description": description, "features": features, "web_link": web_link, "extra_info": extra_info, "images": images})

        printNumberOfPagesScraped(pages)
        loadBuffer()
        index += 24
        
        if index >= numberOfListings:
            break
            
    createOutputs(data, ['price', 'address'], 'buy', 'rightmove')

def getExtraInfoFromListing(listing_info):
    extra_info = ""
    if listing_info:
        if listing_info.get_text(strip=True) != "Premium Listing":
            extra_info = listing_info.get_text(strip=True)
    return extra_info

def getTenure(response):
    property_details = response.find('div', class_='_4hBezflLdgDMdFtURKTWh')
    return property_details.find('div', class_='_32IXcntQDSML3xVUkSdyXN').find('div', class_='_3ZGPwl2N1mHAJH3cbltyWn').get_text(strip=True) if property_details.find('div', class_='_32IXcntQDSML3xVUkSdyXN') else ""


if __name__ == "__main__":
    main()