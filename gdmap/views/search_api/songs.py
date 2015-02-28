from flask.ext.restful import Resource, reqparse

from gdmap import api
from gdmap.es_index import query_es
from gdmap.views.search_api.songs_query_body import build_query_body
from gdmap.views.search_api.songs_format_result import format_result

# Create a parser to parse arguments for the songs endpoint
parser = reqparse.RequestParser()

# Query on all text fields
parser.add_argument('q', type=str)

# Search by song title
parser.add_argument('title', type=str)

# Search by sha1
parser.add_argument('sha1', type=str)

# Search by location name
parser.add_argument('location', type=str)

# Filter by track number
parser.add_argument('track', type=int)

# Results per page
parser.add_argument('per_page', type=int)

# Page number
parser.add_argument('page', type=int)

# Date min
parser.add_argument('date_gte', type=str)

# Date max
parser.add_argument('date_lte', type=str)

# Sort order
parser.add_argument('sort', type=str)
parser.add_argument('sort_order', type=str)


class SongResource(Resource):
    # Define the access point for this resource
    uri = '/api/songs/'

    # Handle HTTP GET requests
    def get(self):
        args = parser.parse_args()
        query_body = build_query_body(args)
        query_result = query_es(query_body)
        formatted_result = format_result(query_result)
        return formatted_result


# Add the endpoint to the search API
api.add_resource(SongResource, SongResource.uri)
