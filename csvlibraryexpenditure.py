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
    
    csv_path = 'static/data/csvlibraryexpenditure.csv'  # Updated to use the new CSV file

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
        height=height if height is not None else 500  # Use provided height or default to 500
    )

    plot_html_library_expenditure = fig_expenditure.to_html(full_html=False)   

    # Render the template with the data for all above codings
    return render_template('csvlibraryexpenditure.html', plot_library_expenditure=plot_html_library_expenditure)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
