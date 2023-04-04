import requests
from bs4 import BeautifulSoup
from .url_stringbuilder import getPurpleBricksBuyString

def main():
    PB_BUY_URL = getPurpleBricksBuyString()
    # set the URL of the page to scrape
    url = 'https://www.purplebricks.co.uk/search/property-for-sale/london'

    # send a GET request to the URL
    response = requests.get(PB_BUY_URL)

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    #print(soup)

    # find the elements on the page that you want to extract data from
    # e.g. the price of the properties
    prices = soup.find_all('strong', {'class': 'property-cardstyled__StyledPrice-sc-15g6092-7 cWDEnM'})
    addresses = soup.find_all('span', {'class': 'property-cardstyled__StyledAddress-sc-15g6092-10 kLxiCm'})
    features = soup.find_all('span', {'class': 'property-cardstyled__StyledTitle-sc-15g6092-9 hpHzPf'})
    web_links = soup.find_all('a', {'class': 'property-cardstyled__StyledLink-sc-15g6092-1 eQIvCR'})

    length = len(prices)

    # iterate over the elements and extract the data
    for price in prices:
        print(price.text.strip())

    for address in addresses:
        print(address.text.strip())
    
    for feature in features:
        print(feature.text.strip())
    
    for web_link in web_links:
        print(f"https://www.purplebricks.co.uk{web_link.get('href')}")

if __name__ == "__main__":
    main()