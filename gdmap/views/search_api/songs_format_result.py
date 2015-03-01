"""Utilities to format songs results from elasticsearch."""


def format_result(es_result, args):
    """Return the formatted songs grouped by show."""
    # Get bucket pagination arguments
    page = args.get('page') or 1
    per_page = args.get('per_page') or 10

    songs_by_shows = []
    show_buckets = es_result['aggregations']['shows']['buckets']

    # Assuming all possible buckets are returned, we'll now pull out the 'page'
    # that we want. Elasticsearch does not allow aggregation pagination as of
    # Elasticsearch 1.4.4, so we'll have to do the pagination in-memory.
    # See https://github.com/elasticsearch/elasticsearch/issues/4915
    start_index = (page - 1) * per_page
    end_index = page * per_page
    show_buckets = show_buckets[start_index: end_index]

    for show_bucket in show_buckets:
        show_name = show_bucket['key']
        songs = show_bucket['shows_hits']['hits']['hits']
        total = show_bucket['shows_hits']['hits']['total']
        # Clean the elasticsearch ids from the songs
        clean_songs = []
        for song in songs:
            clean_songs.append(song['_source'])
        songs_by_shows.append({'show': show_name, 'total': total, 'songs': clean_songs})
    return {'songs_by_show': songs_by_shows}
