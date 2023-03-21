import buy_webscraper
import rent_webscraper

def main():
    print("Running Rightmove Buy Webscraper:")
    buy_webscraper.main()
    print("\nRunning Rightmove Rent Webscraper:")
    rent_webscraper.main()

if __name__ == "__main__":
    main()