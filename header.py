from flask import Flask, render_template
import requests
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

app = Flask(__name__)

@app.route('/')
def index():

## Coding starts here for top header effects

    # Define the API URLs
    #api_url_institute_profile = "https://api.openalex.org/institutions/I16292982"
    
    # Fetch data from the APIs
    response_institution = requests.get(api_url_institute_profile)
    
    # Extract data from the institution API
    institution_data = response_institution.json()
    display_name = institution_data.get('display_name')
    works_count = institution_data.get('works_count')
    cited_by_count = institution_data.get ('cited_by_count')
    h_index = institution_data.get("summary_stats",{}).get("h_index")
    country = institution_data.get("geo", {}).get("country")
    display_name_alternatives = institution_data.get('display_name_alternatives', [])
    
    # Check if there are at least 3 alternatives
    if len(display_name_alternatives) >= 3:
        third_alternative = display_name_alternatives[3]
    else:
        third_alternative = "N/A"  # If there are less than 3 alternatives
        
        # Render the template with the data for all above codings
    return render_template('testall.html', display_name=display_name, works_count=works_count,
    cited_by_count=cited_by_count, h_index=h_index,third_alternative=third_alternative,
    country=country)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)