# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

from flask import Flask, render_template
import requests
import pandas as pd
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

## Read the CSV file for department-wise cost and number of projects

    csv_path = '/opt/datavisuopenalexcsv/static/data/csvdepartmentproject.csv'  # Updated to use CSV file
    
    try:
        df = pd.read_csv(csv_path)  # Read CSV file
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        df = pd.DataFrame()

    # Process the DataFrame to create the bar chart
    df = df.drop_duplicates()  # Remove duplicates if any
    df_sorted = df.sort_values(by='numberofprojects', ascending=False)

    department = df_sorted['department']
    number_of_projects = df_sorted['numberofprojects']
    total_project_cost = df_sorted['totalprojectcost']

    # Create a vertical bar chart using Plotly
    fig_department = go.Figure()

    fig_department.add_trace(go.Bar(x=department, y=number_of_projects, name='No. of Projects',
        marker_color='blue', text=number_of_projects,texttemplate='%{text}', textposition='inside'))

    fig_department.add_trace(go.Bar(x=department, y=total_project_cost, name='Cost (In Lakh)',
        marker_color='green', text=total_project_cost,texttemplate='%{text}', textposition='inside'))

    fig_department.update_layout(title='Projects and Costs by Department',
        xaxis_title='Department', yaxis_title='Count / Cost', barmode='group', paper_bgcolor='#b7908f')
    
    # Increase only the plot area of charts
    fig_department.update_layout(
        margin=dict(l=0, r=0, t=35, b=0), height=350  # Use provided height or default to 500
    )

    plot_html_department = fig_department.to_html(full_html=False)   

    # Render the template with the data for all above codings

    csv_path = '/opt/datavisuopenalexcsv/static/data/csvlibraryexpenditure.csv'  # Updated to use the new CSV file

    try:
        df = pd.read_csv(csv_path)  # Read CSV file
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        df = pd.DataFrame()

    # Process the DataFrame to create the line chart
    df = df.drop_duplicates()  # Remove duplicates if any
    df_sorted = df.sort_values(by='year')  # Sort by year

    year = df_sorted['year']
    expenditure = df_sorted['expenditure']

    # Create a line chart using Plotly
    fig_expenditure = go.Figure()

    fig_expenditure.add_trace(go.Scatter(
        x=year,
        y=expenditure,
        mode='lines+markers+text',  # Include text labels
        name='Expenditure',
        line=dict(color='green', width=3),
        marker=dict(color='royalblue', size=9),
        text=expenditure,  # Display the expenditure values as text
        textposition='middle left',  # Position text labels above the markers
        texttemplate='%{text:.2f}',  # Format text to show 2 decimal places
        textfont=dict(
            family="Arial, sans-serif",  # Font family
            size=13,  # Font size
            color='black'  # Font color
        )
    ))

    fig_expenditure.update_layout(
        title='Library Expenditure on Reading Materials (In Crore)',
        xaxis_title='Year',
        yaxis_title='Expenditure',
        paper_bgcolor='#ff7f00',
        plot_bgcolor='#cbdf04 ',
        xaxis=dict(
            tickvals=year,  # Ensure every year is a tick value
            ticktext=[str(y) for y in year],  # Convert year values to strings for ticks
            tickangle=45  # Optionally rotate x-axis labels to avoid overlap
        ),
        margin=dict(l=10, r=20, t=50, b=50),  # Increased bottom margin for x-axis labels
        height=350 # Use provided height or default to 500
    )

    plot_html_library_expenditure = fig_expenditure.to_html(full_html=False)   

   # Colors for the charts
    colors = '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a'

    csv_path = '/opt/datavisuopenalexcsv/static/data/yearwisetheses.csv'  # Updated to use new CSV file
    
    try:
        df = pd.read_csv(csv_path)  # Read CSV file
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        df = pd.DataFrame()

    # Process the DataFrame to create the bar chart
    df = df.drop_duplicates()  # Remove duplicates if any
    df_sorted = df.sort_values(by='year')  # Sort by year

    year = df_sorted['year']
    number_of_theses = df_sorted['numberoftheses']

    # Create a vertical bar chart using Plotly
    fig_theses = go.Figure()

    fig_theses.add_trace(go.Bar(
        x=year,
        y=number_of_theses,
        name='Number of Theses',
        marker_color=colors,
        text=number_of_theses,  # Display the number of theses as text
        texttemplate='%{text}',  # Format text to show only the values
        textposition='inside'  # Position the text outside the bar
    ))

    fig_theses.update_layout(
        title='Year-Wise Theses Produced',
        xaxis_title='Year',
        yaxis_title='Number of Theses',
        plot_bgcolor='#a4f196',
        paper_bgcolor='#f5f5f5',
        xaxis=dict(
            tickvals=year,  # Ensure every year is a tick value
            ticktext=[str(y) for y in year],  # Convert year values to strings for ticks
            tickangle=45  # Optionally rotate x-axis labels to avoid overlap
        ),
        margin=dict(l=10, r=10, t=35, b=50),  # Increased bottom margin for x-axis labels
        height=350  # Use provided height or default to 500
    )

    plot_html_theses = fig_theses.to_html(full_html=False)   

## Read the Excel file from the static folder

    excel_path = '/opt/datavisuopenalexcsv/static/data/excelprojectsponsor.xlsx'
    sheet_name = 'sponsoringagency'
    
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        df = pd.DataFrame()

    # Process the DataFrame to create the bar chart
    df = df.drop_duplicates()  # Remove duplicates if any
    df_sorted = df.sort_values(by='numberofprojects', ascending=False)

    sponsoring_agencies = df_sorted['sponsoringagency']
    number_of_projects = df_sorted['numberofprojects']
    total_project_cost = df_sorted['totalprojectcost']

    # Create a bar chart using Plotly
    fig_sponsoring_agencies = go.Figure()

    fig_sponsoring_agencies.add_trace(go.Bar(y=sponsoring_agencies,x=number_of_projects, orientation='h',
        name='No. of Projects', marker_color='blue', text=number_of_projects,texttemplate='%{text}', textposition='inside'))

    fig_sponsoring_agencies.add_trace(go.Bar(y=sponsoring_agencies,x=total_project_cost, orientation='h',
        name='Cost (In Lakh)',marker_color='red', text=total_project_cost,texttemplate='%{text}', textposition='inside'))

    fig_sponsoring_agencies.update_layout(title='Projects and Costs by Sponsoring Agency',
        yaxis_title='Sponsoring Agency',xaxis_title='Count / Cost',barmode='group',paper_bgcolor='#94f97e')
    
    # Increase only the plot area of charts
    fig_sponsoring_agencies.update_layout(
        margin=dict(l=0, r=0, t=35, b=0),height=350 ) # Use provided height or default to 400

    plot_html_sponsoring_agencies = fig_sponsoring_agencies.to_html(full_html=False)

    # Render the template with the data for all above codings
    return render_template('dashboard.html', yearly_citation=yearly_citation, geo_map=geo_map, open_access=open_access, 
                           primary_topic=primary_topic, yearly_data=yearly_data, top_citation=top_citation, 
                           heatmap=heatmap, top_author=top_author, funding_agency=funding_agency, 
                           display_name=display_name, works_count=works_count, keywords=keywords, 
                           source_type=source_type, type=type, publications=publications, 
                           cited_by_count=cited_by_count, h_index=h_index, third_alternative=third_alternative,
                           country=country, continent_chart=continent_chart, publisher_chart=publisher_chart,
                           plot_department=plot_html_department,plot_sponsoring_agencies=plot_html_sponsoring_agencies, plot_theses=plot_html_theses,
                           plot_library_expenditure=plot_html_library_expenditure)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=False)
