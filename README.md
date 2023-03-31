# WebScraper

## Fork and clone this repo
After fork (change the "user" to your github username):
> git clone https://github.com/"user"/WebScraper.git

## Install the requirements
On Windows:
> pip3 install -r requirements.txt --user

## To run - open terminal from root folder and run:
> python run_scripts.py

### Note
The [run_scripts.py](./run_scripts.py) file does contain a section of code to create the .env.local file automatically for you (which is what the application uses to retrieve the environment variables) - [this section of code](./run_scripts.py#L7L8) needs uncommenting (removal of the "#" on lines 7 and 8). 

To use the values you require, please make sure to change the values against the variables within the [relevant script](./create_env_script.sh#L10L28) before running the run_scripts file.

--- 

# Usage Instructions
## Environment Variables
You will need to create yourself a .env.local file in the root directory of this repository, similar to the existing [.env](./.env) file, (or otherwise follow the instructions in the Note of the "To run..." step above). Within this file, you will need to define/set the following values:

### RM_URL='https://www.rightmove.co.uk/property-for-sale/find.html?'

### RM_RENT_URL='https://www.rightmove.co.uk/property-to-rent/find.html?'

### RM_LOCATION_REGION=liverpool 
  - any region of the UK - may be useful to verify the location via the region search here (https://www.rightmove.co.uk/house-prices.html), e.g. for liverpool you would see this in the url: https://www.rightmove.co.uk/house-prices/***liverpool***.html
### RM_MAX_BED=
  - 0-10, leave blank for max
### RM_MIN_BED=
  - 0-10, leave blank for min
### RM_MAX_PRICE=260000 
  - leave empty for max price
### RM_MIN_PRICE=50000 
  - leave empty for min price
### RM_RADIUS=3.0
  - leave blank for any, or use:
    - 0.25 
    - 0.5 
    - 1.0 
    - 3.0
    - 5.0 
    - 10.0 
    - 20.0 
    - 30.0 
    - 40.0
### RM_SORT_TYPE=6 
  - 2 - sort by highest price
  - 1 - sort by lowest price
  - 6 - sort by newest listed
  - 10 - sort by oldest listed
### RM_PROPERTY_TYPE=
  - can be left blank for all, or use one or more of the below options (note that if you use multiple, they should be separated in the list using %2C, e.g. "detached%2Csemi-detached%2Cterraced):
    - detached
    - semi-detached
    - terraced
    - bungalow
    - flat
    - land
    - park-home
### RM_MAX_DAYS_SINCE_ADDED=14
  - leave blank for anytime or use the following number of days:
    - 1
    - 3
    - 7
    - 14 
### RM_INCLUDES_STC=false
  - determine if you want to display lots which are Subject to Contact (STC) or Under Offer (UO) or Sold, options are: 
    - true
    - false
### RM_MUST_HAVE=
  - can leave blank to show all, separate each option with "%2C" (e.g. garden%2Cparking), other options include:
    - garden
    - parking
    - newHome
    - retirement
    - sharedOwnership
    - auction
### RM_DONT_SHOW= 
  - can leave blank to show all, separate each option with "%2C" (e.g. retirement%2CsharedOwnership), other options include:
    - retirement
    - sharedOwnership
    - newHome
### RM_FURNISH_TYPE=
  - can be left blank for all, or use one or more of the following (separating with "%2C", e.g. furnished%2CpartFurnished)
    - furnished
    - unfurnished
    - partFurnished
### RM_KEYWORDS=
  - any keyword you require the listing to include
### RM_MAX_PRICE_RENT=40000 
-   price per calendar month (pcm), leave empty for max price
### RM_MIN_PRICE_RENT=0 
  - price per calendar month (pcm), leave empty for min price
### RM_INCLUDE_LA=false
  - determine if you want to display lots which are Let Agreed or Sold, options are: 
    - true
    - false
### RM_LET_TYPE= 
  - shortTerm, longTerm or leave blank for any

---

## Disclaimer
Please note that this project is for **personal use only** - the use of webscrapers is unauthorised by some of the websites used within this project.