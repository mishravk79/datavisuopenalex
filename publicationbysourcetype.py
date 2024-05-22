from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index():

    ## Coding starts here for colors to be applied in all charts

    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#0000FF', '#FF0000', '#00FF80', '#FF8000', '#8000FF', '#80FF00']

    ## Coding starts here for stacked bar chart
    
    # Define the API URL
    #api_url_source_type = "https://api.openalex.org/works?group_by=primary_location.source.type&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
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

            fig.update_layout(
                title='Publication by Source Types',
                xaxis_title='Count',
                yaxis_title='Source Types',
                barmode='stack',
                paper_bgcolor='#000000',
                plot_bgcolor='#000000',
                font=dict(
                    family="Arial, sans-serif",
                    size=14,
                    color="white"
                )
            )

            # Increase only the plot area of charts
            fig.update_layout(
                margin=dict(l=0, r=0, t=40, b=40)
            )

            # Convert the Plotly figure to HTML
            plot_html_source_type = fig.to_html(full_html=False) 

            # Render the template with the data
            return render_template('publicationbysourcetype.html', plot_source_type=plot_html_source_type)
        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
