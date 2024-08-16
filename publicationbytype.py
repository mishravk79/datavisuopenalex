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

    response = requests.get(api_url_type)
    
    if response.status_code == 200:
        data = response.json()
        # Extract data for the donut chart
        data_items = data.get("group_by", [])
        labels = [item.get("key_display_name", "") for item in data_items]
        counts = [item.get("count", 0) for item in data_items]

        # Create donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=counts, hole=0.4)])
        fig.update_layout(title='Publication by Types', paper_bgcolor='#808080', margin=dict(l=5, r=5, t=50, b=5),height=height if height is not None else 500)  # Use provided height or default to 400
        fig.update_traces(textinfo='label+percent', textposition='inside')
        fig.update_traces(marker=dict(colors=['#FFA500', '#FF1493', '#00FFFF', '#FF4500', '#9400D3', '#32CD32', '#FF8C00', '#FF69B4', '#00FF00', '#FFD700', '#8A2BE2', '#00FF7F', '#8B0000', '#1E90FF', '#7FFF00', '#FF00FF', '#0000FF', '#FF0000', '#4B0082']
))

        # Convert the plot to HTML
        plot_html_type = fig.to_html(full_html=False)

        # Render the template with the plot
        return render_template('publicationbytype.html', plot_type=plot_html_type)
    
def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
