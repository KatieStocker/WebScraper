import pandas as pd

def createOutputs(data, sortValues, searchType, scrapeType):
    df = pd.DataFrame(data)

    print("Creating output files...")

    df.sort_values(sortValues, ascending=[True, True]).drop_duplicates('web_link', keep='last').to_csv(f"Output/{scrapeType}_properties_{searchType}.csv", index=False, sep='|')

    df.sort_values(sortValues, ascending=[True, True]).drop_duplicates('web_link', keep='last').to_json(f"Output/{scrapeType}_properties_{searchType}.json", orient='records')
    print("Outputs have been created.")