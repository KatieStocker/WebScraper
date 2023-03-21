import os 
from dotenv import load_dotenv

load_dotenv()

RM_URL = os.getenv('RM_URL')
RM_LOCATION_IDENTIFIER = os.getenv('RM_LOCATION_IDENTIFIER')
RM_MAX_BED = os.getenv('RM_MAX_BED')
RM_MIN_BED = os.getenv('RM_MIN_BED')
RM_MAX_PRICE = os.getenv('RM_MAX_PRICE')
RM_MIN_PRICE = os.getenv('RM_MIN_PRICE')
RM_RADIUS = os.getenv('RM_RADIUS')
RM_SORT_TYPE = os.getenv('RM_SORT_TYPE')
RM_PROPERTY_TYPE = os.getenv('RM_PROPERTY_TYPE')
RM_INCLUDES_STC = os.getenv('RM_INCLUDES_STC')
RM_MUST_HAVE = os.getenv('RM_MUST_HAVE')
RM_DONT_SHOW = os.getenv('RM_DONT_SHOW')
RM_FURNISH_TYPE = os.getenv('RM_FURNISH_TYPE')
RM_KEYWORDS = os.getenv('RM_KEYWORDS')

def getRightmoveBuyString():
    return f"{RM_URL}locationIdentifier={RM_LOCATION_IDENTIFIER}&maxBedrooms={RM_MAX_BED}&minBedrooms={RM_MIN_BED}&maxPrice={RM_MAX_PRICE}&minPrice={RM_MIN_PRICE}&radius={RM_RADIUS}&sortType={RM_SORT_TYPE}&propertyTypes={RM_PROPERTY_TYPE}&includeSSTC={RM_INCLUDES_STC}&mustHave={RM_MUST_HAVE}&dontShow={RM_DONT_SHOW}&furnishTypes={RM_FURNISH_TYPE}&keywords={RM_KEYWORDS}"

def updateIndex(url, index):
    return url.replace(f"&sortType={RM_SORT_TYPE}", f"&sortType={RM_SORT_TYPE}&index={index}")