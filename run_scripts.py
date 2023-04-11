import subprocess
from Rightmove import rightmove_buy_webscraper, rightmove_rent_webscraper
from PurpleBricks import pb_buy_webscraper

def main():

    ## Uncomment the two lines below if you require a .env.local file creating - make sure to change the values against each variable within the create_env_script.sh file with what you require before running!
    # print("Running script to create your environment (.env.local) file...")    
    # subprocess.run(['create_env_script.sh'], shell=True)

    print("Running Rightmove Buy Webscraper:")
    rightmove_buy_webscraper.main()
    print("\nRunning Rightmove Rent Webscraper:")
    rightmove_rent_webscraper.main()
    print("\nRunning PurpleBricks Buy Webscraper:")
    pb_buy_webscraper.main()

if __name__ == "__main__":
    main()