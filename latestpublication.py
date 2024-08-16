# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

import requests
from flask import Flask, render_template
from api_urls import *

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
    # Coding to fetch the latest ten publications
    
    publications = fetch_latest_publications()
    for publication in publications:
        publication['authors'] = ', '.join([author['author']['display_name'] for author in publication.get('authorships', [])])

        return render_template('latestpublication.html', publications=publications)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
