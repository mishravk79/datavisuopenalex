import requests
from flask import Flask, render_template
from api_urls import *

app = Flask(__name__)

def fetch_latest_publications():
    try:
        #api_url_latest_publication = "https://api.openalex.org/works?filter=institutions.id:I56404289&sort=publication_year:desc&per-page=10"
        response = requests.get(api_url_latest_publication)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['results']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching publications: {e}")
        return []

@app.route('/')
def index():
    try:
        publications = fetch_latest_publications()
        for publication in publications:
            publication['authors'] = ', '.join([author['author']['display_name'] for author in publication.get('authorships', [])])
        return render_template('latestpublication.html', publications=publications)
    except Exception as e:
        print(f"Error rendering template: {e}")
        return "An error occurred", 500

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
