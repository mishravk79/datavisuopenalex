# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

from flask import Flask, render_template
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/')
def index(height=None):
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
        margin=dict(l=0, r=0, t=35, b=0), height=height if height is not None else 500  # Use provided height or default to 500
    )

    plot_html_department = fig_department.to_html(full_html=False)   

    # Render the template with the data for all above codings
    return render_template('csvdepartmentproject.html', plot_department=plot_html_department)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
