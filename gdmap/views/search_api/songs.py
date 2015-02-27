from flask import abort
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
        query_body = _build_query_body(args)
        query_result = query_es(query_body)
        formatted_result = _format_result(query_result)
        return formatted_result


def _build_query_body(args):
    multi_field_query = None
    field_queries = []
    # Get page information with defaults
    page = args.get('page') or 1
    per_page = args.get('per_page') or 10
    from_ = (page - 1) * per_page
    query_body = {'from': from_, 'size': per_page}

    # Sort results
    sort_field = args.get('sort', None)
    sort_order = args.get('sort_order') or 'asc'
    if sort_field not in [None, 'title']:
        abort(400)
    if sort_order not in ['asc', 'desc']:
        print "SORT ORDER: %s" % sort_order
        abort(400)
    if sort_field:
        query_body['sort'] = [{sort_field: {"order": sort_order}}]

    # Get multi-field query body
    if args.get('q'):
        multi_field_query = _build_multi_field_query(args.get('q'))
    # Get targeted query bodies
    fields = ['sha1', 'show_id', 'filename', 'album', 'title', 'location', 'track']
    for field in fields:
        if args.get(field):
            phrase = args.get(field)
            field_query = _build_match_query(field, phrase)
            field_queries.append(field_query)
    # Get date filters
    date_gte = args.get('date_gte', None)
    date_lte = args.get('date_lte', None)

    filter_body = _build_date_filter(date_gte, date_lte)
    terms_query = None
    if multi_field_query and field_queries:
        must_queries = field_queries + [multi_field_query]
        terms_query = {
            "bool": {
                "must": must_queries
            }
        }
    elif multi_field_query:
        terms_query = multi_field_query
    elif field_queries:
        terms_query = {
            "bool": {
                "must": field_queries
            }
        }
    else:
        terms_query = {"match_all": {}}
    if filter_body:
        query_body["query"] = {
            "filtered": {
                "query": terms_query,
                "filter": filter_body
            }
        }
    else:
        query_body["query"] = terms_query
    query_body['aggregations'] = _show_aggregations_body(per_page)
    return query_body


def _show_aggregations_body(num_results, hits_per_show=1):
    aggregations_body = {
        "shows": {
            "terms": {
                "field": "album.raw",
                "size": num_results
            },
            "aggregations": {
                "shows_hits": {
                    "top_hits": {
                        "size": hits_per_show
                    }
                }
            }
        }
    }
    return aggregations_body


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


def _build_date_filter(date_gte, date_lte):
    if not date_gte and not date_lte:
        return None
    filter_body = {"range": {"date": {}}}
    if date_gte:
        filter_body["range"]["date"]["gte"] = date_gte
    if date_lte:
        filter_body["range"]["date"]["lte"] = date_lte
    return filter_body


def _format_result(es_result):
    songs_result = _format_songs(es_result)
    songs_by_show_result = _format_songs_by_show(es_result)
    return {'songs': songs_result, 'songs_by_show': songs_by_show_result}


def _format_songs(es_result):
    """Return the formatted songs."""
    total = es_result['hits']['total']
    songs = es_result['hits']['hits']
    # Clean the elasticsearch ids from the songs
    clean_songs = []
    for song in songs:
        data = song['_source']
        clean_songs.append(data)
    return {'total': total, 'songs': clean_songs}


def _format_songs_by_show(es_result):
    """Return the formatted songs grouped by show."""
    songs_by_shows = []
    show_buckets = es_result['aggregations']['shows']['buckets']
    for show_bucket in show_buckets:
        show_name = show_bucket['key']
        songs = show_bucket['shows_hits']['hits']['hits']
        total = show_bucket['shows_hits']['hits']['total']
        # Clean the elasticsearch ids from the songs
        clean_songs = []
        for song in songs:
            clean_songs.append(song['_source'])
        songs_by_shows.append({'show': show_name, 'total': total, 'songs': clean_songs})
    return songs_by_shows


# Add the endpoint to the search API
api.add_resource(SongResource, SongResource.uri)
