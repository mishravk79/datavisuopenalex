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

    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#0000FF', '#FF0000', '#00FF80', '#FF8000', '#8000FF', '#80FF00']

    ## Coding starts here for stacked bar chart
    
  
    # Fetch data from the API
    response = requests.get(api_url_source_type)
    if response.status_code == 200:
        data = response.json()
        
        # Process data for stacked bar chart
        if 'group_by' in data:
            group_by_data = data['group_by']
            source_types = [item['key_display_name'] for item in group_by_data]
            counts = [item['count'] for item in group_by_data]
            
            # Create Plotly stacked bar chart
            fig = go.Figure()

            for i, source_type in enumerate(source_types):
                fig.add_trace(go.Bar(
                    x=[counts[i]],
                    y=[source_type],
                    orientation='h',
                    marker=dict(color=colors[i]),
                    name=source_type,
                    text=[counts[i]],  # Labels with specific count for each source type
                    textposition='auto'  # Automatic placement of labels
    
                ))

                fig.update_yaxes(
                    tickvals=list(range(len(source_types))), ticktext=source_types,
                    title_text='Source Types',
                    showticklabels=False  # Hide tick labels on the y-axis
                )

                fig.update_layout(title='Publication by Source Types', xaxis_title='Count',
                    barmode='stack', paper_bgcolor='#ff9900', plot_bgcolor='#006600',
                    margin=dict(l=5, r=5, t=40, b=5),
                    height=height if height is not None else 500  # Use provided height or default to 400
                )
                
            # Convert the Plotly figure to HTML
            plot_html_source_type = fig.to_html(full_html=False) 

            # Render the template with the data
            return render_template('publicationbysourcetype.html', plot_source_type=plot_html_source_type)
        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)