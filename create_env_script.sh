#! /bin/bash

set -Ee

echo "Creating .env.local file"

cat <<EOF > ./.env.local
RM_URL='https://www.rightmove.co.uk/property-for-sale/find.html?'
RM_RENT_URL='https://www.rightmove.co.uk/property-to-rent/find.html?'
# REPLACE VALUES BELOW AFTER EACH "=" WITH WHAT YOU REQUIRE - USE THE README.md FOR HELP
RM_LOCATION_REGION=london
RM_MAX_BED=10
RM_MIN_BED=1
RM_MAX_PRICE=1000000
RM_MIN_PRICE=
RM_RADIUS=40.0
RM_SORT_TYPE=6
RM_PROPERTY_TYPE=detached%2Csemi-detached%2Cterraced
RM_MAX_DAYS_SINCE_ADDED=14
RM_INCLUDES_STC=false
RM_MUST_HAVE=garden%2Cparking
RM_DONT_SHOW=retirement%2CsharedOwnership
RM_FURNISH_TYPE=furnished%2CpartFurnished
RM_KEYWORDS=
RM_MAX_PRICE_RENT=40000
RM_MIN_PRICE_RENT=
RM_INCLUDE_LA=false
RM_LET_TYPE=shortTerm%2ClongTerm
EOF