from flask import Flask, render_template, url_for, request, g
import sqlite3
from data_mining import usa_brew_df, usa_brew_no_geo_df

# Create App
app = Flask(__name__)

# Create variables to display how many breweries there are in usa
# Including how many breweries have geo locations, and how many do not 
# (for informational purposes for the user)
total_breweries = len(usa_brew_df) + len(usa_brew_no_geo_df)
breweries_with_geo = len(usa_brew_df)
breweries_no_geo = len(usa_brew_no_geo_df)

# Create the route of the home page for the app
@app.route('/', methods = ["GET", "POST"])
def index():
    search = request.form.get('search')
    conn = sqlite3.connect('breweries.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        results = []
        for row in c.execute('SELECT * FROM breweries WHERE name LIKE ?', ('%'+search+'%',)).fetchall():
            results.append(row)
        for row in c.execute('SELECT * FROM breweries WHERE city LIKE ?', ('%'+search+'%',)).fetchall():
            results.append(row)
        for row in c.execute('SELECT * FROM breweries WHERE postal_code LIKE ?', ('%'+search+'%',)).fetchall():
            results.append(row)
        
        breweries = []
        for result in results:
            name = result[1]
            address = result[3] + ", " + result[4] + ", " + result[5] + " " + result[6]
            phone = result[9]
            website = result[10]
            breweries.append([name, address, phone, website])
        
        conn.close()

        return render_template("search.html", breweries=breweries, total_breweries=total_breweries, 
                               breweries_with_geo=breweries_with_geo, breweries_no_geo=breweries_no_geo)
    
    else:
        return render_template('index.html', total_breweries=total_breweries, 
                               breweries_with_geo=breweries_with_geo, breweries_no_geo=breweries_no_geo)


# Create the route of the search results page
@app.route('/search', methods=['GET','POST'])
def search():
    
    search = request.form.get('search')
    conn = sqlite3.connect('breweries.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        results = []
        for row in c.execute('SELECT * FROM breweries WHERE name LIKE ?', ('%'+search+'%',)).fetchall():
            results.append(row)
        for row in c.execute('SELECT * FROM breweries WHERE city LIKE ?', ('%'+search+'%',)).fetchall():
            results.append(row)
        for row in c.execute('SELECT * FROM breweries WHERE postal_code LIKE ?', ('%'+search+'%',)).fetchall():
            results.append(row)
        
        breweries = []
        for result in results:
            name = result[1]
            address = result[3] + ", " + result[4] + ", " + result[5] + " " + result[6]
            phone = result[9]
            website = result[10]
            breweries.append([name, address, phone, website])
        
        conn.close()

        return render_template("search.html", breweries=breweries, total_breweries=total_breweries, 
                               breweries_with_geo=breweries_with_geo, breweries_no_geo=breweries_no_geo)
    
    else:
        return render_template('search.html', total_breweries=total_breweries, 
                               breweries_with_geo=breweries_with_geo, breweries_no_geo=breweries_no_geo)


# Create about route
@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template('about.html')


# Create the route to host the map of the usa breweries
@app.route('/brewmap', methods=["GET", "POST"])
def brewmap():
    return render_template('usa_brew_map.html')


if __name__ == '__main__':
    app.run()