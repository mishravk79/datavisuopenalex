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
    # Colors for the charts
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Fetch data from the API
    response = requests.get(api_url_yearly_citation)
    if response.status_code == 200:
        data = response.json()
        counts_by_year = data.get('counts_by_year', [])
        
        # Filter data for the last ten years
        current_year = datetime.now().year
        last_ten_years_data = [entry for entry in counts_by_year if current_year - entry['year'] < 10]
        
        years = [entry['year'] for entry in last_ten_years_data]
        counts = [entry['cited_by_count'] for entry in last_ten_years_data]
        
        # Create the plot
        fig_yearly_citation = go.Figure(data=[go.Bar(x=years, y=counts, marker_color=colors, text=counts)])
        fig_yearly_citation.update_layout(
            title='Citations Per Year',
            xaxis_title='Year',
            xaxis_tickangle=90,
            xaxis_tickvals=years,
            yaxis_title='Citation Count',
            paper_bgcolor='#DE3163',
            height=height if height is not None else 500  # Use provided height or default to 400
        )
       
        # Adjust layout margins
        fig_yearly_citation.update_layout(
            margin=dict(l=20, r=35, t=35, b=35),
        )
        
        # Convert the plot to HTML
        plot_html_yearly_citation = fig_yearly_citation.to_html(full_html=False)
        
        return render_template('citationsperyear.html', plot_yearly_citation=plot_html_yearly_citation)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
