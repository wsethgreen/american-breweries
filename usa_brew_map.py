import plotly.express as px
import plotly.io as pio
from data_mining import usa_brew_df

# Create the scatter plot
fig = px.scatter_mapbox(usa_brew_df, lat=usa_brew_df.latitude, lon=usa_brew_df.longitude, 
                        size=usa_brew_df.latitude, size_max=6, zoom=3, mapbox_style="carto-positron", 
                        hover_name=usa_brew_df.name, title="USA Breweries", height=450,
                        width=700, text=usa_brew_df.street)

#fig.show()

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

pio.write_html(fig, file='templates/usa_brew_map.html', auto_open=False)

