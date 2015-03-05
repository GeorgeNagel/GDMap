from flask.ext.restful import Resource

from gdmap import api
from gdmap.es_index import query_es
from gdmap.views.search_api.songs_query_body import build_songs_query
from gdmap.views.search_api.songs_format_result import format_songs
from gdmap.views.search_api.parser import parser


class SongResource(Resource):
    # Define the access point for this resource
    uri = '/api/songs/'

    # Handle HTTP GET requests
    def get(self):
        args = parser.parse_args()
        query_body = build_songs_query(args)

        query_result = query_es(query_body)
        formatted_result = format_songs(query_result)
        return formatted_result


# Add the endpoint to the search API
api.add_resource(SongResource, SongResource.uri)
