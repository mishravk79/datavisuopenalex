from flask import Flask, render_template
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from api_urls import *

app = Flask(__name__)

## Coding to fetch the latest ten publications
def fetch_latest_publications():
    try:
        #api_url_latest_publication = "https://api.openalex.org/works?filter=institutions.id:i16292982&sort=publication_year:desc&per-page=10"
        response = requests.get(api_url_latest_publication)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['results']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching publications: {e}")
        return []

@app.route('/')
def index():
    
    
## Coding starts here for colors to be applied in all charts

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    
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
        
       
## Coding starts here for open access data

    # Define the API URLs
    #api_url_open_access = "https://api.openalex.org/works?group_by=open_access.is_oa&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
    # Fetch data from the APIs
    response_open_access = requests.get(api_url_open_access)
    data_open_access = response_open_access.json()
    
    # Extract data for Open Access chart
    group_by_data = data_open_access.get('group_by', [])
    counts = [entry['count'] for entry in group_by_data]
    
    # Create Open Access pie chart
    colors_open_access = ['#1f77b4', '#05c80b']
    labels = ['Others', 'Open Access']
    fig_open_access = go.Figure(data=[go.Pie(labels=labels, values=counts, marker=dict(colors=colors_open_access))])
    fig_open_access.update_layout(title='Open Access Publications', paper_bgcolor=' #c761da ')
    
    # Increase only plot are of open access chart
    fig_open_access.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),  # Open access publication margines
    )
    
    # Convert the chart to html
    plot_html_open_access = fig_open_access.to_html(full_html=False, default_height=250)


## Coding starts here for top ten author contributor

    # Define the API URL
    #api_url_top_author = "https://api.openalex.org/works?group_by=authorships.author.id&per_page=200&filter=authorships.institutions.lineage:i16292982"
  
    # Fetch data from the API
    response_top_author = requests.get(api_url_top_author)
    data_top_author = response_top_author.json()
    
    # Extract data for top author contributors
    group_by_data_top_author = data_top_author.get('group_by', [])
    
    # Sort contributors by count in increasing order
    sorted_top_author = sorted(group_by_data_top_author, key=lambda x: x['count'])
    
    # Take only the top 10 contributors
    top_contributors = sorted_top_author[-10:]
    
    # Extract author names and counts for top contributors
    author = [entry['key_display_name'] for entry in top_contributors]
    counts_top_author = [entry['count'] for entry in top_contributors]
    
    # Create top author contributor bar chart
    fig_top_author = go.Figure(data=[go.Bar(x=counts_top_author, y=author, orientation='h', marker_color=colors, text=counts_top_author, textposition='auto')])
    fig_top_author.update_layout(title='Top Ten Contributor', yaxis_title='Author', xaxis_title='Top author Count', paper_bgcolor=' #54d215 ')

    # Increase only the plot area of charts
    fig_top_author.update_layout(
        margin=dict(l=20, r=35, t=35, b=35),  # Top contributors margins
    )
    
    # Convert the plots to HTML
    plot_html_top_author = fig_top_author.to_html(full_html=False, default_height=250)
 
## Coding starts here for top ten cited articles

    # Define the API URLs
    #api_url_top_citation = "https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i16292982,cited_by_count:500-10000&per_page=10"
 
    # Fetch data from the APIs
    response_top_citation = requests.get(api_url_top_citation)
    data_top_citation = response_top_citation.json()
    
    # Extract data for top citations
    citations_and_counts = [(entry['title'], entry['cited_by_count']) for entry in data_top_citation['results']]
    sorted_citations_and_counts = sorted(citations_and_counts, key=lambda x: x[1])  
    top_citations = [entry[0] for entry in sorted_citations_and_counts]
    cited_by_counts = [entry[1] for entry in sorted_citations_and_counts] 
    
    # Create the top citation bar chart
    fig_top_citation = go.Figure(data=[go.Bar(y=top_citations, x=cited_by_counts,orientation='h', marker_color=colors,text=cited_by_counts, textposition='auto' )])
    fig_top_citation.update_layout(title='Top Ten Cited Publications',yaxis=dict(side='right'), paper_bgcolor='#F4FA58',hoverlabel=dict(font=dict(size=8)))
    
    # Increase only the plot area of charts
    fig_top_citation.update_layout(
        margin=dict(l=10, r=20, t=35, b=50),  # Top cited articles margins
    )
    
    # Convert the plots to HTML
    plot_html_top_citation = fig_top_citation.to_html(full_html=False, default_height=250)
    
## Coding starts here for primary topics/subjects

    # Define the API URLs
    #api_url_primary_topic = "https://api.openalex.org/works?group_by=primary_topic.field.id&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
    # Fetch data from the APIs
    response_primary_topic = requests.get(api_url_primary_topic)
    data_primary_topic = response_primary_topic.json()
    
    # Extract data for primary topics
    group_by_data_primary_topic = data_primary_topic.get('group_by', [])
    
    # Extract labels and values for the primary topic bubble chart
    labels = [entry['key_display_name'] for entry in group_by_data_primary_topic]
    sizes = [entry['count'] for entry in group_by_data_primary_topic]
    
    # Create Bubble chart for primary topic distribution
    fig_primary_topic = go.Figure(data=[go.Scatter(
        x=labels,
        y=[1]*len(labels),  # Assigning a constant y-value for all bubbles
        mode='markers',
        marker=dict(size=sizes,
                    sizemode='area',
                    sizeref=2.*max(sizes)/(50.**2),  # Adjusting bubble sizes
                    sizemin=4),
        
        text=sizes,  # Display values on the bubbles
        textposition='top center',marker_color=colors,  # Position the values on top of the bubble
    )])
    
    # Update layout for the primary topics bubble chart
    fig_primary_topic.update_layout(title='Primary Topics Distribution',
                                    xaxis=dict(title=''),
                                    yaxis=dict(title=''),  # No y-axis label
                                    paper_bgcolor='#FF4000')
    
    # Increase only the plot area of charts
    fig_primary_topic.update_layout(
        margin=dict(l=0, r=0, t=35, b=0),  # Primary topic margines
    )
    
    # Convert the plots to HTML
    plot_html_primary_topic = fig_primary_topic.to_html(full_html=False, default_height=250)   
    
## Coding starts here for funding agency data
    
    # Define the API URLs
    #api_url_funding_agency = "https://api.openalex.org/works?group_by=grants.funder&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
    
    # Fetch data from the APIs
    response_funding_agency = requests.get(api_url_funding_agency)
    data_funding_agency = response_funding_agency.json()
    
    # Extract data for funding agency
    group_by_data_funding_agency = data_funding_agency.get('group_by',[])
    labels = [entry['key_display_name'] for entry in group_by_data_funding_agency]
    quantities = [entry['count'] for entry in group_by_data_funding_agency]
    
    # Create treemap chart for funding agency distribution
    fig_funding_agency = go.Figure(go.Treemap(
        labels=labels,
        parents=['']*len(labels),  # No parent nodes, so all nodes are at the top level
        values=quantities,
    ))
    
    # Update layout for the treemap chart
    fig_funding_agency.update_layout(title='Top Funding Agency Distribution', paper_bgcolor='#000000')
    
    # Increase only the plot area of charts
    fig_funding_agency.update_layout(
        margin=dict(l=0, r=0, t=0, b=0,),  # Top funding agency
    )
    
    # Convert the plots to HTML
    plot_html_funding_agency = fig_funding_agency.to_html(full_html=False, default_height=250)     
    
## Coding for latest ten year wise citation data 
    
    # define the api urls
    #api_url_yearly_citation = "https://api.openalex.org/institutions/I16292982"
    
    # Fetch data from the APIs
    response = requests.get(api_url_yearly_citation)
    if response.status_code == 200:
        data = response.json()
        counts_by_year = data.get('counts_by_year', [])
        
    # Filter data for the last ten years
        current_year = datetime.now().year
        last_ten_years_data = [entry for entry in counts_by_year if current_year - entry['year'] < 10]
        
        years = [entry['year'] for entry in last_ten_years_data]
        counts = [entry['cited_by_count'] for entry in last_ten_years_data]
        
        fig_yearly_citation = go.Figure(data=[go.Bar(x=years, y=counts, marker_color=colors, text=counts)])
        fig_yearly_citation.update_layout(title='Citations Per Year', xaxis_title='Year',xaxis_tickangle=90,xaxis_tickvals=years, yaxis_title='Citation Count',paper_bgcolor='#DE3163')
       
    
    # Increase only the plot area of charts
    fig_yearly_citation.update_layout(
        margin=dict(l=20, r=35, t=35, b=35,),  # yearly citation
    )
    # Convert the plots to HTML
    plot_html_yearly_citation = fig_yearly_citation.to_html(full_html=False, default_height=250)     

## Coding for latest ten yearwise Publication data 
    
    #define the api urls
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
    plot_html_yearly_data = fig_yearly_data.to_html(full_html=False, default_height=250)            

## Coding for the geomap chart to display country wide colaborations

    # Define the API URL for the geomap chart
    #api_url_geo_map = "https://api.openalex.org/works?group_by=authorships.countries&per_page=200&filter=authorships.countries:countries/in,authorships.institutions.lineage:i16292982"

    # Fetch data from the API for the geomap chart
    response_geo_map = requests.get(api_url_geo_map)
    data_geo_map = response_geo_map.json()

    # Extract data for the geomap chart
    countries = [entry['key_display_name'] for entry in data_geo_map['group_by']]
    counts = [entry['count'] for entry in data_geo_map['group_by']]

    # Create a choropleth map
    fig_geo_map = go.Figure(data=go.Choropleth(
        locations=countries,  # Country names
        z=counts,  # Data to be color-coded
        locationmode='country names',  # Set location mode to country names
        colorscale='YlOrRd',  # Choose a colorscale
        colorbar_title='Count',  # Set colorbar title
        
    ))

    # Update layout for the geomap chart
    fig_geo_map.update_layout(
        title='Counts by Country',
        geo=dict(
        showcoastlines=True,  # Show coastlines on the map
        bgcolor='#0a15c2',
        ),
    )
   
    # Increase only the plot area of charts
    fig_geo_map.update_layout(
        margin=dict(l=10, r=0, t=0, b=0,),  # map size
    )
    # Convert the plot to HTML
    plot_html_geo_map = fig_geo_map.to_html(full_html=False, default_height=250)
    
## Coding for the top ten collaborator institutes

    # URL for fetching data
    #api_url_ten_collaborator = "https://api.openalex.org/works?group_by=authorships.institutions.lineage&per_page=200&filter=authorships.institutions.lineage:i16292982"

    ## Fetch data from the API
    response = requests.get(api_url_ten_collaborator)
    if response.status_code == 200:
        data = response.json()
        collaborators_data = data.get('group_by', [])
        
        if len(collaborators_data) > 1:
            parent_institute = collaborators_data[0]
            your_institute_name = parent_institute['key_display_name']
            your_institute_count = parent_institute['count']
            
            top_collaborators = sorted(collaborators_data[1:], key=lambda x: x['count'], reverse=True)[:10]
            
            collaborator_names = [entry['key_display_name'] for entry in top_collaborators]
            collaboration_counts = [entry['count'] for entry in top_collaborators]
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=[collaboration_counts],
                x=collaborator_names,
                hovertemplate='Collaborator: %{x}<br>Count: %{z}<extra></extra>',
                colorscale='Rainbow'))

            fig_heatmap.update_layout(
                title='Top Ten Collaborator Institutes',
                xaxis_title='',
                yaxis_title='',
                #yaxis=dict(title=f"{your_institute_name} ({your_institute_count})", showticklabels=False),
                paper_bgcolor='#fbc039',
                plot_bgcolor='#d3d3d3')

            plot_html_heatmap = fig_heatmap.to_html(full_html=False, default_height=250)
            
## Coding for the publications by Source Type (stacked bar chart) 

    #Colors to be applied in this charts

    source_type_colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#00FF00', '#0000FF', '#FF0000', '#00FF80', '#FF8000', '#8000FF', '#80FF00']

    # Define the API URL
    #api_url_source_type = "https://api.openalex.org/works?group_by=primary_location.source.type&per_page=200&filter=authorships.institutions.lineage:i16292982"
    
    # Fetch data from the API
    response = requests.get(api_url_source_type)
    if response.status_code == 200:
        data = response.json()
        
        # Process data for stacked bar chart
        if 'group_by' in data:
            group_by_data = data['group_by']
            source_types = [item['key_display_name'] for item in group_by_data]
            counts = [item['count'] for item in group_by_data]
            
            # Create Plotly stacked bar chart
            fig = go.Figure()

            for i, source_type in enumerate(source_types):
                fig.add_trace(go.Bar(
                    x=[counts[i]],
                    y=[source_type],
                    orientation='h',
                    marker=dict(color=source_type_colors[i]),
                    name=source_type,
                    text=[counts[i]],  # Labels with specific count for each source type
                    textposition='auto',  # Automatic placement of labels
                        
                ))
                
                fig.update_yaxes(
                    tickvals=list(range(len(source_types))), ticktext=source_types,
                    title_text='Source Types',
                    showticklabels=False  # Hide tick labels on the y-axis
                )

                fig.update_layout(title='Publication by Source Types', xaxis_title='Count',
                    barmode='stack', paper_bgcolor='#FF0000', plot_bgcolor='#006600',
                    margin=dict(l=5, r=5, t=40, b=5)
                )
            
            # Convert the Plotly figure to HTML
            plot_html_source_type = fig.to_html(full_html=False, default_height=250) 
            
## Coding for the publications by keywords (key word cloud)   

    # Define the API URL
    #api_url_keywords = "https://api.openalex.org/works?group_by=keywords.id&per_page=200&filter=authorships.institutions.lineage:i16292982"

    # Fetch data from the API
    response = requests.get(api_url_keywords)
    data = response.json()

    # Extract keywords and their counts
    try:
        results = data.get('group_by', [])
        keywords_and_counts = [(entry['key_display_name'], entry['count']) for entry in results]
    except KeyError as e:
        print("KeyError:", e)
        return "Error: KeyError occurred. Check the JSON response structure."

    # Create word and count lists for Plotly
    words = [entry[0] for entry in keywords_and_counts]
    counts = [entry[1] for entry in keywords_and_counts]

    # Create the word cloud chart
    fig = go.Figure(data=go.Scatter(x=words, y=counts, mode='markers', marker=dict(
        size=counts,
        color=counts,
        colorscale='Jet',
        showscale=True
    )))

    fig.update_layout(title='Publication by Keywords',paper_bgcolor='#00ffff',
                    margin=dict(l=5, r=5, t=50, b=5))
    
    # Convert the plot to HTML
    plot_html_keywords = fig.to_html(full_html=False, default_height=250)
    
## Coding for publication by Types

    # Fetch data from the API
    #api_url_type = "https://api.openalex.org/works?group_by=type&per_page=200&filter=authorships.institutions.lineage:i16292982"
    response = requests.get(api_url_type)
    
    if response.status_code == 200:
        data = response.json()
        # Extract data for the donut chart
        data_items = data.get("group_by", [])
        labels = [item.get("key_display_name", "") for item in data_items]
        counts = [item.get("count", 0) for item in data_items]

        # Create donut chart
        fig = go.Figure(data=[go.Pie(labels=labels, values=counts, hole=0.4)])
        fig.update_layout(title='Publication by Types', paper_bgcolor='#808080', margin=dict(l=5, r=5, t=50, b=5))
        fig.update_traces(textinfo='label+percent', textposition='inside')
        fig.update_traces(marker=dict(colors=['#FFA500', '#FF1493', '#00FFFF', '#FF4500', '#9400D3', '#32CD32', '#FF8C00', '#FF69B4', '#00FF00', '#FFD700', '#8A2BE2', '#00FF7F', '#8B0000', '#1E90FF', '#7FFF00', '#FF00FF', '#0000FF', '#FF0000', '#4B0082']
))

        # Convert the plot to HTML
        plot_html_type = fig.to_html(full_html=False, default_height=250)
        
## Coding to fetch the latest ten publications
        publications = fetch_latest_publications()
        for publication in publications:
            publication['authors'] = ', '.join([author['author']['display_name'] for author in publication.get('authorships', [])])


## Read the Excel file for sponsoring agency cost and number

    excel_path = 'static/local_data.xlsx'
    sheet_name = 'sponsoringagency'
    
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        df = pd.DataFrame()

    # Process the DataFrame to create the bar chart
    df = df.drop_duplicates()  # Remove duplicates if any
    df_sorted = df.sort_values(by='Number of Projects', ascending=False)

    sponsoring_agencies = df_sorted['Sponsoring Agency']
    number_of_projects = df_sorted['Number of Projects']
    total_project_cost = df_sorted['total Project Cost (In Lakh)']

    # Create a bar chart using Plotly
    fig_sponsoring_agencies = go.Figure()

    fig_sponsoring_agencies.add_trace(go.Bar(y=sponsoring_agencies,x=number_of_projects, orientation='h',
        name='No. of Projects', marker_color='blue'))

    fig_sponsoring_agencies.add_trace(go.Bar(y=sponsoring_agencies,x=total_project_cost, orientation='h',
        name='Cost (In Lakh)',marker_color='red'))

    fig_sponsoring_agencies.update_layout(title='Projects and Costs by Sponsoring Agency',
        yaxis_title='Sponsoring Agency',xaxis_title='Count / Cost',barmode='group',paper_bgcolor='#94f97e')
    
    # Increase only the plot area of charts
    fig_sponsoring_agencies.update_layout(
        margin=dict(l=0, r=0, t=35, b=0), )

    plot_html_sponsoring_agencies = fig_sponsoring_agencies.to_html(full_html=False, default_height=250)

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

    plot_html_department = fig_department.to_html(full_html=False, default_height=250)

# Render the template with the data for all above codings
    return render_template('dashboard.html', plot_geo_map=plot_html_geo_map, plot_yearly_data=plot_html_yearly_data, display_name=display_name, works_count=works_count,
    cited_by_count=cited_by_count, h_index=h_index,third_alternative=third_alternative,
    country=country, plot_open_access=plot_html_open_access, plot_top_author=plot_html_top_author,plot_top_citation=plot_html_top_citation, plot_primary_topic=plot_html_primary_topic, 
    plot_funding_agency=plot_html_funding_agency,plot_yearly_citation=plot_html_yearly_citation,plot_heatmap=plot_html_heatmap, plot_source_type=plot_html_source_type,
    plot_keywords=plot_html_keywords, plot_type=plot_html_type, publications=publications, plot_sponsoring_agencies=plot_html_sponsoring_agencies,
    plot_department=plot_html_department)

def application(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
