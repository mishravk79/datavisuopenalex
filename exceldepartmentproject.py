from flask import Flask, render_template
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index():
    
    
 ## Read the Excel file for department wise cost and number of project

    excel_path = 'static/local_data.xlsx'
    sheet_name = 'department'
    
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        df = pd.DataFrame()

    # Process the DataFrame to create the bar chart
    df = df.drop_duplicates()  # Remove duplicates if any
    df_sorted = df.sort_values(by='Number of Projects', ascending=False)

    department = df_sorted['Department']
    number_of_projects = df_sorted['Number of Projects']
    total_project_cost = df_sorted['Total Project Cost (In Lakh)']

    # Create a bar chart using Plotly
    fig_department = go.Figure()

    fig_department.add_trace(go.Bar(y=department,x=number_of_projects, orientation='h',
        name='No. of Projects', marker_color='blue'))

    fig_department.add_trace(go.Bar(y=department,x=total_project_cost, orientation='h',
        name='Cost (In Lakh)',marker_color='green'))

    fig_department.update_layout(title='Projects and Costs by Department',
        yaxis_title='Department',xaxis_title='Count / Cost',barmode='group',paper_bgcolor='#b7908f')
    
    # Increase only the plot area of charts
    fig_department.update_layout(
        margin=dict(l=0, r=0, t=35, b=0), )

    plot_html_department = fig_department.to_html(full_html=False)   

  

# Render the template with the data for all above codings
    return render_template('exceldepartmentproject.html',plot_department=plot_html_department)        


def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)