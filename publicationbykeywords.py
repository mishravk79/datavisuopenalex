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
## Coding for the publications by keywords (key word cloud)   

    # Fetch data from the API
    response = requests.get(api_url_keywords)
    data = response.json()

    # Extract keywords and their counts
    try:
        results = data.get('group_by', [])
        keywords_and_counts = [(entry['key_display_name'], entry['count']) for entry in results]
    except KeyError as e:
        print("KeyError:", e)
        return "Error: KeyError occurred. Check the JSON response structure."

    # Create word and count lists for Plotly
    words = [entry[0] for entry in keywords_and_counts]
    counts = [entry[1] for entry in keywords_and_counts]

    # Create the word cloud chart
    fig = go.Figure(data=go.Scatter(x=words, y=counts, mode='markers', marker=dict(
        size=counts,
        color=counts,
        colorscale='Jet',
        showscale=True
    )))

    fig.update_layout(title='Publication by Keywords',paper_bgcolor='#00ffff',
                    margin=dict(l=5, r=5, t=50, b=5),
                    height=height if height is not None else 600  # Use provided height or default to 400
)
    
    # Convert the plot to HTML
    plot_html_keywords = fig.to_html(full_html=False)

    # Render the template with the plot HTML
    return render_template('publicationbykeywords.html', plot_keywords=plot_html_keywords)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
