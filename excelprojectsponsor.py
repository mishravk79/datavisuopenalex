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

app = Flask(__name__)

@app.route('/')
def index(height=None):
    
    
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
        margin=dict(l=0, r=0, t=35, b=0),height=height if height is not None else 500 ) # Use provided height or default to 400

    plot_html_sponsoring_agencies = fig_sponsoring_agencies.to_html(full_html=False)

# Render the template with the data for all above codings
    return render_template('excelprojectsponsor.html',plot_sponsoring_agencies=plot_html_sponsoring_agencies)        


def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
