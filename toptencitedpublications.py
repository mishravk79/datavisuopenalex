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


## Coding starts here for top ten cited articles

    # Define the API URLs
    #api_url_top_citation = "https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i16292982,cited_by_count:500-10000&per_page=10"
 
    # Fetch data from the APIs
    response_top_citation = requests.get(api_url_top_citation)
    data_top_citation = response_top_citation.json()
    
    # Extract data for top citations
    citations_and_counts = [(entry['title'], entry['cited_by_count']) for entry in data_top_citation['results']]
    sorted_citations_and_counts = sorted(citations_and_counts, key=lambda x: x[1])  
    top_citations = [entry[0] for entry in sorted_citations_and_counts]
    cited_by_counts = [entry[1] for entry in sorted_citations_and_counts] 
    
    # Create the top citation bar chart
    fig_top_citation = go.Figure(data=[go.Bar(y=top_citations, x=cited_by_counts,orientation='h', marker_color=colors,text=cited_by_counts, textposition='auto' )])
    fig_top_citation.update_layout(title='Top Ten Cited Publications',yaxis=dict(side='right'), paper_bgcolor='#F4FA58',hoverlabel=dict(font=dict(size=8)))
    
    # Increase only the plot area of charts
    fig_top_citation.update_layout(
        margin=dict(l=10, r=20, t=35, b=50),  # Top cited articles margins
    )
    
    # Convert the plots to HTML
    plot_html_top_citation = fig_top_citation.to_html(full_html=False) 
    
    
    # Render the template with the data for all above codings
    return render_template('toptencitedpublications.html',plot_top_citation=plot_html_top_citation)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)