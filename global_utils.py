import pandas as pd
import random
import time

def createOutputs(data, sortValues, searchType, scrapeType):
    df = pd.DataFrame(data)

    print("Creating output files...")

    df.sort_values(sortValues, ascending=[True, True]).drop_duplicates('web_link', keep='last').to_csv(f"Output/{scrapeType}_properties_{searchType}.csv", index=False, sep='|')

    df.sort_values(sortValues, ascending=[True, True]).drop_duplicates('web_link', keep='last').to_json(f"Output/{scrapeType}_properties_{searchType}.json", orient='records')
    print("Outputs have been created.")

def formatPrice(priceString, replaceValue):
    return int(priceString.replace(replaceValue, "").replace("£", "").replace(",",""))

def loadBuffer():
    # code to ensure that we do not overwhelm the website
    time.sleep(random.randint(1, 3))

def printNumberOfPagesScraped(pages):
    numberOfPages = pages + 1
    print(f"You have scraped through {numberOfPages} {'page' if numberOfPages == 1 else 'pages'}")