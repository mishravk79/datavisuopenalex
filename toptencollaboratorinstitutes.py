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


## Coding for the top ten collaborator institutes


    ## Fetch data from the API
    response = requests.get(api_url_ten_collaborator)
    if response.status_code == 200:
        data = response.json()
        collaborators_data = data.get('group_by', [])
        
        if len(collaborators_data) > 1:
            parent_institute = collaborators_data[0]
            your_institute_name = parent_institute['key_display_name']
            your_institute_count = parent_institute['count']
            
            top_collaborators = sorted(collaborators_data[1:], key=lambda x: x['count'], reverse=True)[:10]
            
            collaborator_names = [entry['key_display_name'] for entry in top_collaborators]
            collaboration_counts = [entry['count'] for entry in top_collaborators]
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=[collaboration_counts],
                x=collaborator_names,
                hovertemplate='Collaborator: %{x}<br>Count: %{z}<extra></extra>',
                colorscale='Rainbow'))

            fig_heatmap.update_layout(
                title='Top Ten Collaborator Institutes',
                xaxis_title='',
                yaxis_title='',
                #yaxis=dict(title=f"{your_institute_name} ({your_institute_count})", showticklabels=False),
                paper_bgcolor='#fbc039',
                plot_bgcolor='#d3d3d3',
                height=height if height is not None else 500  # Use provided height or default to 400

                )

            plot_html_heatmap = fig_heatmap.to_html(full_html=False)
    
    
    # Render the template with the data for all above codings
    return render_template('toptencollaboratorinstitutes.html',plot_heatmap=plot_html_heatmap)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)