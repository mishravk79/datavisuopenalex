# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

# codings to fetch data from the different python file names

from citationsperyear import index as plot_yearly_citation
from colaborationwithcountries import index as plot_geo_map
from openaccesspublication import index as plot_open_access
from primarytopicsdistribution import index as plot_primary_topic
from publicationperyear import index as plot_yearly_data
from toptencitedpublications import index as plot_top_citation
from toptencollaboratorinstitutes import index as plot_heatmap
from toptencontributors import index as plot_top_author
from toptenfundingagency import index as plot_funding_agency
from publicationbykeywords import index as plot_keywords
from publicationbysourcetype import index as plot_source_type
from publicationbytype import index as plot_type
from continentwisepublication import index as plot_continent_chart
from publisherwisechart import index as plot_publisher_chart
from csvdepartmentproject import index as plot_department
from excelprojectsponsor import index as plot_sponsoring_agencies
from csvyearwisetheses import index as plot_theses
from csvlibraryexpenditure import index as plot_library_expenditure

app = Flask(__name__)

## Coding to fetch the latest twenty publications
def fetch_latest_publications():
    try:
        response = requests.get(api_url_latest_publication)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['results']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching publications: {e}")
        return []


@app.route('/')
def index():
    
## codes for fetching data from other files
    yearly_citation = plot_yearly_citation(height=250)  # Use the function from citationsperyear.py
    geo_map = plot_geo_map(height=250)  # Import other functions as needed
    open_access = plot_open_access(height=250)
    primary_topic = plot_primary_topic(height=250)
    yearly_data = plot_yearly_data(height=250)
    top_citation = plot_top_citation(height=250)
    heatmap = plot_heatmap(height=250)
    top_author = plot_top_author(height=250)
    funding_agency = plot_funding_agency(height=250)
    keywords = plot_keywords(height=250)
    source_type = plot_source_type(height=250)
    type = plot_type(height=250)
    continent_chart = plot_continent_chart(height=250)
    publisher_chart = plot_publisher_chart(height=250)
    department_project = plot_department(height=350)
    sponsoring_agency = plot_sponsoring_agencies(height=350)
    theses = plot_theses(height=350)
    library_expenditure = plot_library_expenditure(height=350)

    # Define the API URLs
    
    # Fetch data from the APIs
    response_institution = requests.get(api_url_institute_profile)
    
    # Extract data from the institution API
    institution_data = response_institution.json()
    display_name = institution_data.get('display_name')
    works_count = institution_data.get('works_count')
    cited_by_count = institution_data.get('cited_by_count')
    h_index = institution_data.get("summary_stats", {}).get("h_index")
    country = institution_data.get("geo", {}).get("country")
    display_name_alternatives = institution_data.get('display_name_alternatives', [])
    
    # Check if there are at least 3 alternatives
    if len(display_name_alternatives) >= 3:
        third_alternative = display_name_alternatives[2]  # Note: index 2 for the third item
    else:
        third_alternative = "N/A"  # If there are less than 3 alternatives
        
# Coding to fetch the latest ten publications
    publications = []
    publications = fetch_latest_publications()
    for publication in publications:
        publication['authors'] = ', '.join([author['author']['display_name'] for author in publication.get('authorships', [])])

   
    return render_template('test.html', yearly_citation=yearly_citation, geo_map=geo_map, open_access=open_access, 
                           primary_topic=primary_topic, yearly_data=yearly_data, top_citation=top_citation, 
                           heatmap=heatmap, top_author=top_author, funding_agency=funding_agency, 
                           display_name=display_name, works_count=works_count, keywords=keywords, 
                           source_type=source_type, type=type, publications=publications, 
                           cited_by_count=cited_by_count, h_index=h_index, third_alternative=third_alternative,
                           country=country, continent_chart=continent_chart, publisher_chart=publisher_chart,
                           department_project=department_project,sponsoring_agency=sponsoring_agency, theses=theses,
                           library_expenditure=library_expenditure)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
