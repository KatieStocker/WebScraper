import os 
from dotenv import load_dotenv
import requests, re
import json

load_dotenv()

RM_URL = os.getenv('RM_URL')
RM_RENT_URL = os.getenv('RM_RENT_URL')
RM_LOCATION_REGION = os.getenv('RM_LOCATION_REGION')
RM_MAX_BED = os.getenv('RM_MAX_BED')
RM_MIN_BED = os.getenv('RM_MIN_BED')
RM_MAX_PRICE = os.getenv('RM_MAX_PRICE')
RM_MIN_PRICE = os.getenv('RM_MIN_PRICE')
RM_MAX_PRICE_RENT = os.getenv('RM_MAX_PRICE_RENT')
RM_MIN_PRICE_RENT = os.getenv('RM_MIN_PRICE_RENT')
RM_RADIUS = os.getenv('RM_RADIUS')
RM_SORT_TYPE = os.getenv('RM_SORT_TYPE')
RM_PROPERTY_TYPE = os.getenv('RM_PROPERTY_TYPE')
RM_MAX_DAYS_SINCE_ADDED = os.getenv('RM_MAX_DAYS_SINCE_ADDED')
RM_INCLUDES_STC = os.getenv('RM_INCLUDES_STC')
RM_INCLUDE_LA = os.getenv('RM_INCLUDE_LA')
RM_MUST_HAVE = os.getenv('RM_MUST_HAVE')
RM_DONT_SHOW = os.getenv('RM_DONT_SHOW')
RM_FURNISH_TYPE = os.getenv('RM_FURNISH_TYPE')
RM_LET_TYPE = os.getenv('RM_LET_TYPE')
RM_KEYWORDS = os.getenv('RM_KEYWORDS')

def getLocationIdentifierString():
    location = updateLocationIdentifierId(f'https://www.rightmove.co.uk/house-prices/{RM_LOCATION_REGION.lower()}.html')
    return f'REGION^{location}'

# REGION search only currently - will implement POSTCODE separately in the future
# can search based on region (e.g. https://www.rightmove.co.uk/house-prices/liverpool.html), would then need to change the location identifier to use REGION^{location}
# can search based on postcode (e.g. https://www.rightmove.co.uk/house-prices/l3-6bn.html), would need to change the location identifier to use POSTCODE^{location}
def getRightmoveBuyString():
    RM_LOCATION_IDENTIFIER = getLocationIdentifierString()

    return f"{RM_URL}locationIdentifier={RM_LOCATION_IDENTIFIER}&maxBedrooms={RM_MAX_BED}&minBedrooms={RM_MIN_BED}&maxPrice={RM_MAX_PRICE}&minPrice={RM_MIN_PRICE}&radius={RM_RADIUS}&sortType={RM_SORT_TYPE}&propertyTypes={RM_PROPERTY_TYPE}&maxDaysSinceAdded={RM_MAX_DAYS_SINCE_ADDED}&includeSSTC={RM_INCLUDES_STC}&mustHave={RM_MUST_HAVE}&dontShow={RM_DONT_SHOW}&furnishTypes={RM_FURNISH_TYPE}&keywords={RM_KEYWORDS}"

def getRightmoveRentString():
    RM_LOCATION_IDENTIFIER = getLocationIdentifierString()

    return f"{RM_RENT_URL}locationIdentifier={RM_LOCATION_IDENTIFIER}&maxBedrooms={RM_MAX_BED}&minBedrooms={RM_MIN_BED}&maxPrice={RM_MAX_PRICE_RENT}&minPrice={RM_MIN_PRICE_RENT}&radius={RM_RADIUS}&sortType={RM_SORT_TYPE}&propertyTypes={RM_PROPERTY_TYPE}&maxDaysSinceAdded={RM_MAX_DAYS_SINCE_ADDED}&includeLetAgreed={RM_INCLUDE_LA}&mustHave={RM_MUST_HAVE}&dontShow={RM_DONT_SHOW}&furnishTypes={RM_FURNISH_TYPE}&letType={RM_LET_TYPE}&keywords={RM_KEYWORDS}"

def updateIndex(url, index):
    return url.replace(f"&sortType={RM_SORT_TYPE}", f"&sortType={RM_SORT_TYPE}&index={index}")

# converts the location passed to an id, for use in the url string
def updateLocationIdentifierId(location):   
    html_text = requests.get(location).text
    data = re.search(r"__PRELOADED_STATE__ = ({.*?})<", html_text)
    data = json.loads(data.group(1))
    location_id = data["searchLocation"]["locationId"]
    return location_id