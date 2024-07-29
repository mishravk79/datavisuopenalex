from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index():
    
    ## Continent wise publications/collaborations

# Define the API URL for the pie chart
    #api_url_continent_chart = "https://api.openalex.org/works?group_by=authorships.institutions.continent&per_page=200&filter=authorships.institutions.lineage:i16292982"

    # Fetch data from the API for the pie chart
    response_pie_chart = requests.get(api_url_continent_chart)
    data_pie_chart = response_pie_chart.json()

    # Extract data for the pie chart
    continents = [entry['key_display_name'] for entry in data_pie_chart['group_by']]
    counts = [entry['count'] for entry in data_pie_chart['group_by']]

    # Create a pie chart
    fig_continent_chart = go.Figure(data=go.Pie(
        labels=continents,  # Continent names
        values=counts,  # Data to be displayed in the pie chart
        marker=dict(colors=['#8c564b','#ff007f', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#d62728', '#17becf', '#bcbd22', '#e377c2', '#8c564b'])
    ))

    # Update layout for the pie chart
    fig_continent_chart.update_layout(title='Collaboration by Continents', paper_bgcolor='#CD7F32', margin=dict(l=0, r=0, t=0, b=0)
    )

    # Convert the plot to HTML
    plot_html_continent_chart = fig_continent_chart.to_html(full_html=False)

    # Render the template with the data for the pie chart
    return render_template('continentwisepublication.html', plot_continent_chart=plot_html_continent_chart)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)