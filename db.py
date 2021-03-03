import sqlite3
import pandas as pd
from data_mining import usa_brew_df, usa_brew_no_geo_df

# Combine both dataframes to include one dataframe of all breweries in usa

all_usa_brew_df = pd.concat([usa_brew_df, usa_brew_no_geo_df], ignore_index=True)

# Create database

conn = sqlite3.connect('breweries.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS breweries (
        id integer, 
        name text, 
        brewery_type text, 
        street text, 
        city text, 
        state text, 
        postal_code integer,
        longitude real, 
        latitude real, 
        phone text, 
        website_url text
        )""")

conn.commit()

all_usa_brew_df.to_sql('breweries', conn, if_exists='replace', index=False)

# Uncomment the line below to test queries

# for row in c.execute("SELECT * FROM breweries WHERE name LIKE ?", ('%'+'columbus'+'%',)):
#     print(row)

conn.close()