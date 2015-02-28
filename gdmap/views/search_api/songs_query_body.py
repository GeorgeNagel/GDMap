"""Utilities to assist in building the songs query body."""
from flask import abort


def build_query_body(args):
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
                "size": num_results,
                "order": {
                    "top_hit_score": "desc"
                }
            },
            "aggregations": {
                "shows_hits": {
                    # Return the top matching song per "album"
                    "top_hits": {
                        "size": hits_per_show
                    }
                },
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
