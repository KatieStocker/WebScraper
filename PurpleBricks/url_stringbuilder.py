import os 
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('./.env.local')
load_dotenv(dotenv_path=dotenv_path)

PB_URL = os.getenv('PB_URL')
PB_PAGE = os.getenv('PB_PAGE')
PB_SORT_BY = os.getenv('PB_SORT_BY')
PB_STYLE = os.getenv('PB_STYLE')
PB_LOCATION = os.getenv('PB_LOCATION')
PB_RADIUS = os.getenv('PB_RADIUS')
PB_SEARCH_TYPE = os.getenv('PB_SEARCH_TYPE')
PB_SOLD_OR_LET = os.getenv('PB_SOLD_OR_LET')
PB_MIN_PRICE = os.getenv('PB_MIN_PRICE')
PB_MAX_PRICE = os.getenv('PB_MAX_PRICE')
PB_MIN_BED = os.getenv('PB_MIN_BED')
PB_MAX_BED = os.getenv('PB_MAX_BED')
PB_TYPE = os.getenv('PB_TYPE')

def getPurpleBricksBuyString():
    return f"{PB_URL}page={PB_PAGE}&sortBy={PB_SORT_BY}&style={PB_STYLE}&location={PB_LOCATION}&searchRadius={PB_RADIUS}&searchType={PB_SEARCH_TYPE}&soldOrLet={PB_SOLD_OR_LET}&priceFrom={PB_MIN_PRICE}&priceTo={PB_MAX_PRICE}&bedroomsFrom={PB_MIN_BED}&bedroomsTo={PB_MAX_BED}&type={PB_TYPE}&betasearch=true"


def updatePageNumber(url, pageNumber):
    return url.replace(f"page={PB_PAGE}", f"page={pageNumber}")
