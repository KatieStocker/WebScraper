import pandas as pd
import random
import requests
import time
from bs4 import BeautifulSoup
from datetime import date, timedelta

def createOutputs(data, sortValues, searchType):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    print("Creating output files...")
    df.sort_values(sortValues, ascending=[True, True]).drop_duplicates('web_link', keep='last').to_csv(f"Output/rightmove_properties_{searchType}.csv", index=False, sep='|')
    df.sort_values(sortValues, ascending=[True, True]).drop_duplicates('web_link', keep='last').to_json(f"Output/rightmove_properties_{searchType}.json", orient='records')
    print("Outputs have been created.")

def extractDate(date_updated):
    return date_updated.replace("Added on ", "").replace("Added ", "").replace("Reduced on ", "").replace("Reduced ", "")

def formatDateAvailable(string_type, la_date):
    if string_type == "Let available date" and la_date == "Now":
        today_date = date.today().strftime("%d/%m/%Y")
        la_date = today_date

    return la_date

def formatLettingDetailTitle(detail):
    detail = detail.replace("Min.", "Minimum").replace(" ", "_").lower()
    return detail

def formatLettingDetailValue(value):
    value = value.replace("£", "").replace(",", "")
    return value

def formatPrice(priceString, replaceValue):
    return int(priceString.replace(replaceValue, "").replace("£", "").replace(",",""))

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

def getDateUpdatedFromSoup(soup):
    return getDateUpdated(soup.find('div', class_='_2nk2x6QhNB1UrxdI5KpvaF'))

def getDateUpdatedType(date_updated):
    date_updated_type = "Added"
    if date_updated:
        if "Reduced" in date_updated:
            date_updated_type = "Reduced"
    else:
        date_updated_type = ""

    return date_updated_type

def getImagesFromListing(response, imageList):
    initial_images = response.find("div", class_="_2TqQt-Hr9MN0c0wH7p7Z5p").find_all("div", class_="_2uGNfP4v5SSYyfx3rZngKM")

    for item in initial_images:
        imageList.append(item.find("img").get('src'))


def loadBuffer():
    # code to ensure that we do not overwhelm the website
    time.sleep(random.randint(1, 3))

def printNumberOfPagesScraped(pages):
    numberOfPages = pages + 1
    print(f"You have scraped through {numberOfPages} {'page' if numberOfPages == 1 else 'pages'}")