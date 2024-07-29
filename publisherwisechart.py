from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index():
    # Define the API URL for the data
    #api_url_publisher_chart = "https://api.openalex.org/works?group_by=primary_location.source.publisher_lineage&per_page=20&filter=authorships.institutions.lineage:i16292982"

    # Fetch data from the API
    response = requests.get(api_url_publisher_chart)
    data = response.json()

    # Extract data for the bar chart
    publishers = [entry['key_display_name'] for entry in data['group_by']]
    counts = [entry['count'] for entry in data['group_by']]

    # Define a bright color palette for the bar chart
    colors = ['#ff007f', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']

    # Create a bar chart
    fig_publisher_chart = go.Figure(data=go.Bar(
        x=publishers,  # Publisher names
        y=counts,      # Counts
        marker=dict(color=colors),  # Bright colors
    ))

    # Update layout for the bar chart
    fig_publisher_chart.update_layout(
        title='Publication Counts by Top 20 Publisher',
        xaxis_title='Publisher',
        yaxis_title='Publication Count',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        paper_bgcolor='#DAF7A6'
    )

    # Convert the plot to HTML
    plot_html_publisher_chart = fig_publisher_chart.to_html(full_html=False)

    # Render the template with the bar chart data
    return render_template('publisherwisechart.html', plot_publisher_chart=plot_html_publisher_chart)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
