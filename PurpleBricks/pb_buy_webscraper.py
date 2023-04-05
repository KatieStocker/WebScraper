import requests
from bs4 import BeautifulSoup
from .url_stringbuilder import getPurpleBricksBuyString

def main():
    PB_BUY_URL = getPurpleBricksBuyString()

    index = 0
    data = []

    # send a GET request to the URL
    response = requests.get(PB_BUY_URL)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # find the elements on the page that you want to extract data from
    # e.g. the price of the properties
    prices = soup.find_all('strong', {'class': 'property-cardstyled__StyledPrice-sc-15g6092-7 cWDEnM'})
    addresses = soup.find_all('span', {'class': 'property-cardstyled__StyledAddress-sc-15g6092-10 kLxiCm'})
    features = soup.find_all('span', {'class': 'property-cardstyled__StyledTitle-sc-15g6092-9 hpHzPf'})
    web_links = soup.find_all('a', {'class': 'property-cardstyled__StyledLink-sc-15g6092-1 eQIvCR'})

    initialiseDataObject(data, len(prices))

    populateDataObject(prices, "price", data)
    populateDataObject(addresses, "address", data)
    populateDataObject(features, "features", data)
    populateDataObject(web_links, "web_link", data)


def initialiseDataObject(data, length):
    count = 0
    while count < length:
        data.append({"price": "", "address": "", "features": "", "web_link": ""})
        count+=1

def populateDataObject(items, itemType, dataObject):
    count = 0
    for item in items:
        stringToAppend = ""
        if itemType == "web_link":
            stringToAppend = f"https://www.purplebricks.co.uk{item.get('href')}"
        else:
            stringToAppend = item.text.strip()

        dataObject[count][itemType] = stringToAppend
        count += 1
    

if __name__ == "__main__":
    main()