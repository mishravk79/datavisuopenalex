# Copyright (c) 2024 Vinod Kumar Mishra
# This file is part of Datavisuopenalex.
# Datavisuopenalex is released under the MIT License.
# See the License file for more details.

# common api_urls.py file fetched by other python files to display the charts

# Define the common ID
institution_id = "i16292982"

# URLs using the common ID
api_url_institute_profile = f"https://api.openalex.org/institutions/{institution_id}"
api_url_open_access = f"https://api.openalex.org/works?group_by=open_access.is_oa&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_top_author = f"https://api.openalex.org/works?group_by=authorships.author.id&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_top_citation = f"https://api.openalex.org/works?page=1&filter=authorships.institutions.lineage:{institution_id},cited_by_count:500-10000&per_page=10"
api_url_primary_topic = f"https://api.openalex.org/works?group_by=primary_topic.field.id&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_funding_agency = f"https://api.openalex.org/works?group_by=grants.funder&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_yearly_citation = f"https://api.openalex.org/institutions/{institution_id}"
api_url_yearly_data = f"https://api.openalex.org/institutions/{institution_id}"
api_url_geo_map = f"https://api.openalex.org/works?group_by=authorships.countries&per_page=200&filter=authorships.countries:countries/in,authorships.institutions.lineage:{institution_id}"
api_url_ten_collaborator = f"https://api.openalex.org/works?group_by=authorships.institutions.lineage&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_source_type = f"https://api.openalex.org/works?group_by=primary_location.source.type&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_keywords = f"https://api.openalex.org/works?group_by=keywords.id&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_type = f"https://api.openalex.org/works?group_by=type&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_latest_publication = f"https://api.openalex.org/works?filter=institutions.id:{institution_id}&sort=publication_year:desc&per-page=20"
api_url_continent_chart = f"https://api.openalex.org/works?group_by=authorships.institutions.continent&per_page=200&filter=authorships.institutions.lineage:{institution_id}"
api_url_publisher_chart = f"https://api.openalex.org/works?group_by=primary_location.source.publisher_lineage&per_page=20&filter=authorships.institutions.lineage:{institution_id}"
