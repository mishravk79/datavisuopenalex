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


## Coding starts here for open access data

    # Define the API URLs
    #api_url_open_access = "https://api.openalex.org/works?group_by=open_access.is_oa&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
    # Fetch data from the APIs
    response_open_access = requests.get(api_url_open_access)
    data_open_access = response_open_access.json()
    
    # Extract data for Open Access chart
    group_by_data = data_open_access.get('group_by', [])
    counts = [entry['count'] for entry in group_by_data]
    
    # Create Open Access pie chart
    colors_open_access = ['#1f77b4', '#05c80b']
    labels = ['Others', 'Open Access']
    fig_open_access = go.Figure(data=[go.Pie(labels=labels, values=counts, marker=dict(colors=colors_open_access))])
    fig_open_access.update_layout(title='Open Access Publications', paper_bgcolor=' #c761da ')
    
    # Increase only plot are of open access chart
    fig_open_access.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),  # Open access publication margines
    )
    
    # Convert the chart to html
    plot_html_open_access = fig_open_access.to_html(full_html=False)
    
    
    # Render the template with the data for all above codings
    return render_template('openaccesspublication.html',plot_open_access=plot_html_open_access)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)