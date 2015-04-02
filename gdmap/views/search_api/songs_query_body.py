"""Utilities to assist in building the songs query body."""
from flask import abort


def build_songs_query(args):
    query_body = _build_query_body(args)
    # Add pagination and sorting, modifying query_body in-place
    query_sort(query_body, args)
    query_pagination(query_body, args)
    return query_body


def build_songs_by_show_query(args):
    query_body = _build_query_body(args)
    query_body['aggregations'] = aggregations_body(args, 'album.raw', 'shows')
    # Don't return any hits, just aggregations
    query_body['size'] = 0
    return query_body


def build_recordings_query(args):
    query_body = _build_query_body(args)
    query_body['aggregations'] = aggregations_body(args, 'show_id', 'recordings')
    # Don't return any hits, just aggregations
    query_body['size'] = 0
    return query_body


def _build_query_body(args):
    multi_field_query = None
    field_queries = []

    # Get multi-field query body
    if args.get('q'):
        multi_field_query = _build_multi_field_query(args.get('q'))
    # Get targeted query bodies
    fields = ['sha1', 'filename', 'title', 'location', 'track']
    for field in fields:
        if args.get(field):
            phrase = args.get(field)
            field_query = _build_match_query(field, phrase)
            field_queries.append(field_query)
    # Get date filters
    date_gte = args.get('date_gte')
    date_lte = args.get('date_lte')

    date_filter_body = _build_date_filter(date_gte, date_lte)

    # Get album filter
    album = args.get('album')
    album_filter_body = _build_album_filter(album)

    # Get show_id filter
    show_id = args.get('show_id')
    show_id_filter_body = _build_show_id_filter(show_id)

    filter_body = _build_filter(date_filter_body, album_filter_body, show_id_filter_body)

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
    query_body = {}
    if filter_body:
        query_body["query"] = {
            "filtered": {
                "query": terms_query,
                "filter": filter_body
            }
        }
    else:
        query_body["query"] = terms_query
    return query_body


def query_sort(query_body, args):
    """Add sorting for raw songs results (non-aggregated).
    Modifies query_body in-place.
    """
    # Sort results
    sort_field = args.get('sort') or None
    sort_order = args.get('sort_order') or 'desc'
    if sort_field not in [None, 'title', 'date']:
        abort(400)
    if sort_order not in ['asc', 'desc']:
        abort(400)
    if sort_field:
        query_body['sort'] = [{sort_field: {"order": sort_order}}]


def query_pagination(query_body, args):
    """Add pagination for raw songs results (non-aggregated).
    Modifies query_body in-place.
    """
    per_page = args.get('per_page') or 10
    page = args.get('page') or 1

    query_body['from'] = (page - 1) * per_page
    query_body['size'] = per_page


def aggregations_body(args, field_to_aggregate, aggregation_name, hits_per_bucket=1):
    # Get sort information with defaults
    sort_field = args.get('sort') or 'relevance'
    sort_order = args.get('sort_order') or 'desc'
    aggregations_body = {
        aggregation_name: {
            "terms": {
                "field": field_to_aggregate,
                # Return all buckets and paginate them in format_result()
                "size": 0,
                "order": _aggregation_sort(sort_field, sort_order)
            },
            "aggregations": {
                # Return the score of the top matching song per "album"
                "top_hit_score": {
                    "max": {
                        "script": "_score"
                    }
                },
                "top_hit_date": {
                    "avg": {
                        "field": "date"
                    }
                }
            }
        }
    }
    if hits_per_bucket:
        # Add top hits results in each bucket
        aggregations_body[aggregation_name]['aggregations']['%s_hits' % aggregation_name] = {
            "top_hits": {
                "size": hits_per_bucket
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
            ],
            # Use AND to prevent "Me and My Uncle" from showing up
            # in "Uncle John's Band" searches
            "operator": "and",
            # Perform the AND operation across fields, so that searches
            # like "Cassidy Arena" can match against title and venue
            "type": "cross_fields"
        }
    }


def _build_match_query(field, phrase):
    return {
        "match": {
            field: phrase
        }
    }


def _aggregation_sort(sort_field, sort_order):
    """Sort aggregation buckets"""
    if sort_field not in ['relevance', 'date']:
        abort(400)
    if sort_order not in ['asc', 'desc']:
        abort(400)
    if sort_field == 'relevance':
        return {'top_hit_score': sort_order}
    elif sort_field == 'date':
        return {'top_hit_date': sort_order}


def _build_filter(date_filter_body, album_filter_body, show_id_filter_body):
    sub_filters = [filt for filt in [date_filter_body, album_filter_body, show_id_filter_body] if filt]
    if len(sub_filters) > 1:
        filter_body = {"and": sub_filters}
        return filter_body
    elif len(sub_filters) == 1:
        return sub_filters[0]
    else:
        return None


def _build_date_filter(date_gte, date_lte):
    if not date_gte and not date_lte:
        return None
    filter_body = {"range": {"date": {}}}
    if date_gte:
        filter_body["range"]["date"]["gte"] = date_gte
    if date_lte:
        filter_body["range"]["date"]["lte"] = date_lte
    return filter_body


def _build_album_filter(album):
    if not album:
        return None
    return {"term": {"album.raw": album}}


def _build_show_id_filter(show_id):
    if not show_id:
        return None
    return {"term": {"show_id": show_id}}
