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


## Coding for latest ten yearwise Publication data 

    #api_url_yearly_data = "https://api.openalex.org/institutions/I16292982"
    
    # Fetch data from the APIs
    response = requests.get(api_url_yearly_data)
    if response.status_code == 200:
        data = response.json()
        counts_by_year = data.get('counts_by_year', [])
        
    # Filter data for the last ten years
        current_year = datetime.now().year
        last_ten_years_data = [entry for entry in counts_by_year if current_year - entry['year'] < 10]
        
        years = [entry['year'] for entry in last_ten_years_data]
        counts = [entry['works_count'] for entry in last_ten_years_data]
        
        fig_yearly_data = go.Figure(data=[go.Bar(x=years, y=counts, marker_color=colors, text=counts)])
        fig_yearly_data.update_layout(title='Publications Per Year', xaxis_title='Year',xaxis_tickangle=90,xaxis_tickvals=years, yaxis_title='Publication Count',paper_bgcolor='#17becf')
        plot_html_yearly_data = fig_yearly_data.to_html(full_html=False)
    
    # Increase only the plot area of charts
    fig_yearly_data.update_layout(
        margin=dict(l=20, r=35, t=35, b=35,),  # yearly citation
    )
    # Convert the plots to HTML
    plot_html_yearly_data = fig_yearly_data.to_html(full_html=False) 
    
    # Render the template with the data for all above codings
    return render_template('publicationperyear.html',plot_yearly_data=plot_html_yearly_data)        

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)