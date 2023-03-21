from Rightmove import rightmove_buy_webscraper, rightmove_rent_webscraper

def main():
    print("Running Rightmove Buy Webscraper:")
    rightmove_buy_webscraper.main()
    print("\nRunning Rightmove Rent Webscraper:")
    rightmove_rent_webscraper.main()

if __name__ == "__main__":
    main()