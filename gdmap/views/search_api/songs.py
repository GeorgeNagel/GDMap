from flask.ext.restful import Resource, reqparse

from gdmap import api
from gdmap.es_index import query_es

# Create a parser to parse arguments for the songs endpoint
parser = reqparse.RequestParser()

# Search by song title
parser.add_argument('title', type=str)

# Search by sha1
parser.add_argument('sha1', type=str)


class SongResource(Resource):
    # Define the access point for this resource
    uri = '/api/songs/'

    # Handle HTTP GET requests
    def get(self):
        args = parser.parse_args()
        if args.get('sha1'):
            query_body = {
                "query": {
                    "match": {
                        "sha1": args['sha1']
                    }
                }
            }
        elif args.get('title'):
            query_body = {
                "query": {
                    "match": {
                        "title": args['title']
                    }
                }
            }
        else:
            query_body = {"query": {"match_all": {}}}
        query_result = query_es(query_body)
        return query_result

# Add the endpoint to the search API
api.add_resource(SongResource, SongResource.uri)
