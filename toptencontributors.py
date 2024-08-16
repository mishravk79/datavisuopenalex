# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index(height=None):
    ## Coding starts here for colors to be applied in all charts
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    ## Coding starts here for top ten author contributor

    # Fetch data from the API
    response_top_author = requests.get(api_url_top_author)
    data_top_author = response_top_author.json()
    
    # Extract data for top author contributors
    group_by_data_top_author = data_top_author.get('group_by', [])
    
    # Sort contributors by count in increasing order
    sorted_top_author = sorted(group_by_data_top_author, key=lambda x: x['count'])
    
    # Take only the top 10 contributors
    top_contributors = sorted_top_author[-10:]
    
    # Extract author names and counts for top contributors
    author = [entry['key_display_name'] for entry in top_contributors]
    counts_top_author = [entry['count'] for entry in top_contributors]
    
    # Create top author contributor bar chart
    fig_top_author = go.Figure(data=[go.Bar(x=counts_top_author, y=author, orientation='h', marker_color=colors, text=counts_top_author, textposition='auto')])
    fig_top_author.update_layout(title='Top Ten Contributor', yaxis_title='Author', xaxis_title='Top author Count', paper_bgcolor=' #54d215 ')

    # Increase only the plot area of charts
    fig_top_author.update_layout(
        margin=dict(l=20, r=35, t=35, b=35),  # Top contributors margins
        height=height if height is not None else 500  # Use provided height or default to 400

    )
    
    # Convert the plot to HTML
    plot_html_top_author = fig_top_author.to_html(full_html=False)
    
    # Render the template with the plot HTML
    return render_template('toptencontributors.html', plot_top_author=plot_html_top_author)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
