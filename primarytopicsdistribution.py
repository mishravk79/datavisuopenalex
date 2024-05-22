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


## Coding starts here for primary topics/subjects

    # Define the API URLs
    #api_url_primary_topic = "https://api.openalex.org/works?group_by=primary_topic.field.id&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
    # Fetch data from the APIs
    response_primary_topic = requests.get(api_url_primary_topic)
    data_primary_topic = response_primary_topic.json()
    
    # Extract data for primary topics
    group_by_data_primary_topic = data_primary_topic.get('group_by', [])
    
    # Extract labels and values for the primary topic bubble chart
    labels = [entry['key_display_name'] for entry in group_by_data_primary_topic]
    sizes = [entry['count'] for entry in group_by_data_primary_topic]
    
    # Create Bubble chart for primary topic distribution
    fig_primary_topic = go.Figure(data=[go.Scatter(
        x=labels,
        y=[1]*len(labels),  # Assigning a constant y-value for all bubbles
        mode='markers',
        marker=dict(size=sizes,
                    sizemode='area',
                    sizeref=2.*max(sizes)/(50.**2),  # Adjusting bubble sizes
                    sizemin=4),
        
        text=sizes,  # Display values on the bubbles
        textposition='top center',marker_color=colors,  # Position the values on top of the bubble
    )])
    
    # Update layout for the primary topics bubble chart
    fig_primary_topic.update_layout(title='Primary Topics Distribution',
                                    xaxis=dict(title=''),
                                    yaxis=dict(title=''),  # No y-axis label
                                    paper_bgcolor='#FF4000')
    
    # Increase only the plot area of charts
    fig_primary_topic.update_layout(
        margin=dict(l=0, r=0, t=35, b=0),  # Primary topic margines
    )
    
    # Convert the plots to HTML
    plot_html_primary_topic = fig_primary_topic.to_html(full_html=False)   
    
    
    # Render the template with the data for all above codings
    return render_template('primarytopicsdistribution.html',plot_primary_topic=plot_html_primary_topic)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)