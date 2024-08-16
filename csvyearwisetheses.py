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
    
    # Colors for the charts
    colors = '#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a'

    csv_path = 'static/data/yearwisetheses.csv'  # Updated to use new CSV file
    
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
        height=height if height is not None else 500  # Use provided height or default to 500
    )

    plot_html_theses = fig_theses.to_html(full_html=False)   

    # Render the template with the data for all above codings
    return render_template('csvyearwisetheses.html', plot_theses=plot_html_theses)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
