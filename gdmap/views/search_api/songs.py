from flask.ext.restful import Resource, reqparse

from gdmap import api
from gdmap.es_index import query_es

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


class SongResource(Resource):
    # Define the access point for this resource
    uri = '/api/songs/'

    # Handle HTTP GET requests
    def get(self):
        args = parser.parse_args()
        query_body = _build_query_body(args)
        import logging
        logging.warning("QUERY: %s" % query_body)
        query_result = query_es(query_body)
        return query_result


def _build_query_body(args):
    multi_field_query = None
    field_queries = []
    if args.get('q'):
        multi_field_query = _build_multi_field_query(args.get('q'))
    fields = ['sha1', 'show_id', 'filename', 'album', 'title', 'location', 'track']
    for field in fields:
        if args.get(field):
            phrase = args.get(field)
            field_query = _build_match_query(field, phrase)
            field_queries.append(field_query)
    if multi_field_query and field_queries:
        must_queries = field_queries + [multi_field_query]
        query_body = {
            "query": {
                "bool": {
                    "must": must_queries
                }
            }
        }
    elif multi_field_query:
        query_body = {
            "query": multi_field_query
        }
    elif field_queries:
        query_body = {
            "query": {
                "bool": {
                    "must": field_queries
                }
            }
        }
    else:
        query_body = {"query": {"match_all": {}}}
    return query_body


def _build_multi_field_query(phrase):
    return {
        "multi_match": {
            "query": phrase,
            "fields": [
                "sha1", "show_id", "filename",
                "album", "title", "location"
            ]
        }
    }


def _build_match_query(field, phrase):
    return {
        "match": {
            field: phrase
        }
    }

# Add the endpoint to the search API
api.add_resource(SongResource, SongResource.uri)
