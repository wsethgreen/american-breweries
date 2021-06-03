import requests
import json
import pandas as pd


# Base API Call url
base_url = 'https://raw.githubusercontent.com/openbrewerydb/openbrewerydb/master/breweries.json'

# Call API for each state
beer_json_data = requests.get(base_url).json()

# Create Dictionary to house USA Breweries data

usa_brew = {
    'obdb_id': [],
    'name': [],
    "brewery_type": [],
    "street": [],
    "city": [],
    "state": [],
    "postal_code": [],
    "longitude": [],
    "latitude": [],
    "phone": [],
    "website_url": [],
    }

# Create a dictionary to house the breweries who don't have lats/longs

usa_brew_no_geo = {
    'obdb_id': [],
    'name': [],
    "brewery_type": [],
    "street": [],
    "city": [],
    "state": [],
    "postal_code": [],
    "longitude": [],
    "latitude": [],
    "phone": [],
    "website_url": [],
    }

# Create list of keys that I want to extract data for

keys = ['obdb_id', 'name', 'brewery_type', 'street', 'city', 'state', 
        'postal_code', 'longitude', 'latitude', 'phone', 'website_url']

# Extract data from json and add it to dictionary

for record in beer_json_data:
    if record['latitude'] != None or record['latitude'] != "":
        for key in keys:
            usa_brew[key].append(record[key])
    if record['latitude'] == None or record['latitude'] == "":
        for key in keys:
            usa_brew_no_geo[key].append(record[key])


# Convert dictionaries to dfs

usa_brew_df = pd.DataFrame.from_dict(usa_brew)
usa_brew_no_geo_df = pd.DataFrame.from_dict(usa_brew_no_geo)

# determine the indices of all breweries in usa_brew_df with no latitudes 
# and delete them from the usa_brew_df
index_names = usa_brew_df[ usa_brew_df['latitude'] == '' ].index 
usa_brew_df.drop(index_names, inplace=True)

# Note: There is no need to add the breweries with no latitude
# to the usa_brew_no_geo_df. For whatever reason, the data pulled 
# correctly into usa_brew_no_geo_df


# Convert the latitudes and longitudes to floats

usa_brew_df['latitude'] = usa_brew_df['latitude'].apply(lambda x: float(x))
usa_brew_df['longitude'] = usa_brew_df['longitude'].apply(lambda x: float(x))

# Reformat phone numbers so they are easier to read

def phone_format(phone):
    if len(phone) > 1:
        area_code = phone[0:3]
        first_3 = phone[3:6]
        last_4 = phone[-4:]
        return area_code + '-' + first_3 + '-' + last_4
    else:
        return 'n/a'

usa_brew_df['phone'] = usa_brew_df['phone'].apply(lambda x: phone_format(x))
usa_brew_no_geo_df['phone'] = usa_brew_no_geo_df['phone'].apply(lambda x: phone_format(x))

# Update website urls so they are https rather than http

def url_format(url):
    if len(url) > 1:
        http = url[0:4]
        domain = url[4:]
        return http + 's' + domain
    else:
        return 'n/a'

usa_brew_df['website_url'] = usa_brew_df['website_url'].apply(lambda x: url_format(x))
usa_brew_no_geo_df['website_url'] = usa_brew_no_geo_df['website_url'].apply(lambda x: url_format(x))
