import requests
from bs4 import BeautifulSoup
from .url_stringbuilder import getPurpleBricksBuyString, updatePageNumber
from global_utils import createOutputs, formatPrice, loadBuffer, printNumberOfPagesScraped

def main():
    PB_BUY_URL = getPurpleBricksBuyString()

    index = 1
    data = []

    for pages in range(50):
        url = updatePageNumber(PB_BUY_URL, index)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # find the elements on the page that you want to extract data from
        # e.g. the price of the properties
        prices = soup.find_all('strong', {'class': 'property-cardstyled__StyledPrice-sc-15g6092-7 cWDEnM'})
        addresses = soup.find_all('span', {'class': 'property-cardstyled__StyledAddress-sc-15g6092-10 kLxiCm'})
        features = soup.find_all('span', {'class': 'property-cardstyled__StyledTitle-sc-15g6092-9 hpHzPf'})
        web_links = soup.find_all('a', {'class': 'property-cardstyled__StyledLink-sc-15g6092-1 eQIvCR'})

        initialiseDataObject(data, len(prices))

        populateDataObject(prices, "price", data, pages)
        populateDataObject(addresses, "address", data, pages)
        populateDataObject(features, "features", data, pages)
        populateDataObject(web_links, "web_link", data, pages)

        lastPage = getLastPageNumber(soup)
        printNumberOfPagesScraped(pages)
        loadBuffer()

        if lastPage == index:
            break
        index += 1

    createOutputs(data, ['price', 'address'], 'buy', 'purplebricks')


def getLastPageNumber(soup):
    paginationSection = soup.find('div', class_='search-resultsstyled__StyledResultsContainer-krg5hu-0 kiVMLJ').find('ol', class_='pagination-controlsstyled__StyledContainer-sxmx16-0 bySxTQ')
    paginationList = paginationSection.find_all('li')
    lastPage = paginationList[len(paginationList) - 2]
    return int(lastPage.text)

def initialiseDataObject(data, length):
    count = 0
    while count < length:
        data.append({"price": "", "address": "", "features": "", "web_link": ""})
        count+=1

def populateDataObject(items, itemType, dataObject, index):
    count = 0 + (index * 10)
    for item in items:
        stringToAppend = ""
        if itemType == "web_link":
            stringToAppend = f"https://www.purplebricks.co.uk{item.get('href')}"
        else:
            stringToAppend = item.text.strip()

            if itemType == "price":
                stringToAppend = formatPrice(stringToAppend, "")

        dataObject[count][itemType] = stringToAppend
        count += 1

if __name__ == "__main__":
    main()