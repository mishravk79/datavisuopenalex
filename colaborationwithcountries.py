from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index():
    

## Coding starts here for colors to be applied in all charts

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


## Coding for the geomap chart to display country wide colaborations

    # Define the API URL for the geomap chart
    #api_url_geo_map = "https://api.openalex.org/works?group_by=authorships.countries&per_page=200&filter=authorships.countries:countries/in,authorships.institutions.lineage:i16292982"

    # Fetch data from the API for the geomap chart
    response_geo_map = requests.get(api_url_geo_map)
    data_geo_map = response_geo_map.json()

    # Extract data for the geomap chart
    countries = [entry['key_display_name'] for entry in data_geo_map['group_by']]
    counts = [entry['count'] for entry in data_geo_map['group_by']]

    # Create a choropleth map
    fig_geo_map = go.Figure(data=go.Choropleth(
        locations=countries,  # Country names
        z=counts,  # Data to be color-coded
        locationmode='country names',  # Set location mode to country names
        colorscale='YlOrRd',  # Choose a colorscale
        colorbar_title='Count',  # Set colorbar title
        
    ))

    # Update layout for the geomap chart
    fig_geo_map.update_layout(
        title='Counts by Country',
        geo=dict(
        showcoastlines=True,  # Show coastlines on the map
        bgcolor='#0a15c2',
        ),
    )
   
    # Increase only the plot area of charts
    fig_geo_map.update_layout(
        margin=dict(l=10, r=0, t=0, b=0,),  # map size
    )
    # Convert the plot to HTML
    plot_html_geo_map = fig_geo_map.to_html(full_html=False)
    
    
    # Render the template with the data for all above codings
    return render_template('colaborationwithcountries.html',plot_geo_map=plot_html_geo_map)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)