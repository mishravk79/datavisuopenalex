# common api_urls.py file fetched by other python files to display the charts

api_url_institute_profile = "https://api.openalex.org/institutions/I16292982"
api_url_open_access = "https://api.openalex.org/works?group_by=open_access.is_oa&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_top_author = "https://api.openalex.org/works?group_by=authorships.author.id&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_top_citation = "https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:i16292982,cited_by_count:500-10000&per_page=10"
api_url_primary_topic = "https://api.openalex.org/works?group_by=primary_topic.field.id&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_funding_agency = "https://api.openalex.org/works?group_by=grants.funder&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_yearly_citation = "https://api.openalex.org/institutions/I16292982"
api_url_yearly_data = "https://api.openalex.org/institutions/I16292982"
api_url_geo_map = "https://api.openalex.org/works?group_by=authorships.countries&per_page=200&filter=authorships.countries:countries/in,authorships.institutions.lineage:i16292982"
api_url_ten_collaborator = "https://api.openalex.org/works?group_by=authorships.institutions.lineage&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_source_type = "https://api.openalex.org/works?group_by=primary_location.source.type&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_keywords = "https://api.openalex.org/works?group_by=keywords.id&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_type = "https://api.openalex.org/works?group_by=type&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_latest_publication = "https://api.openalex.org/works?filter=institutions.id:i16292982&sort=publication_year:desc&per-page=10"
api_url_continent_chart = "https://api.openalex.org/works?group_by=authorships.institutions.continent&per_page=200&filter=authorships.institutions.lineage:i16292982"
api_url_publisher_chart = "https://api.openalex.org/works?group_by=primary_location.source.publisher_lineage&per_page=20&filter=authorships.institutions.lineage:i16292982"
