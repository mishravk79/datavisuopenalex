# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index(height=None):
    

## Coding starts here for colors to be applied in all charts

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


## Coding starts here for funding agency data
    
    # Fetch data from the APIs
    response_funding_agency = requests.get(api_url_funding_agency)
    data_funding_agency = response_funding_agency.json()
    
    # Extract data for funding agency
    group_by_data_funding_agency = data_funding_agency.get('group_by',[])
    labels = [entry['key_display_name'] for entry in group_by_data_funding_agency]
    quantities = [entry['count'] for entry in group_by_data_funding_agency]
    
    # Create treemap chart for funding agency distribution
    fig_funding_agency = go.Figure(go.Treemap(
        labels=labels,
        parents=['']*len(labels),  # No parent nodes, so all nodes are at the top level
        values=quantities,
    ))
    
    # Update layout for the treemap chart
    fig_funding_agency.update_layout(title='Funding Agency Distribution', paper_bgcolor='#000000')
    
    # Increase only the plot area of charts
    fig_funding_agency.update_layout(
        margin=dict(l=0, r=0, t=0, b=0,),  # Top Ten funding agency
        height=height if height is not None else 500  # Use provided height or default to 400

    )
    
    # Convert the plots to HTML
    plot_html_funding_agency = fig_funding_agency.to_html(full_html=False) 
    
    # Render the template with the data for all above codings
    return render_template('toptenfundingagency.html',plot_funding_agency=plot_html_funding_agency)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)