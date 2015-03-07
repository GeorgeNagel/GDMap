"""Utilities to format songs results from elasticsearch."""


def format_songs_by_show(es_result, args):
    """Return the formatted songs grouped by show."""
    show_buckets = _paginate_aggregation(es_result, args, 'shows')
    songs_by_shows = []
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


def format_recordings(es_result, args):
    """Return the formatted recording info."""
    recording_buckets = _paginate_aggregation(es_result, args, 'recordings')
    recordings = []
    for recording_bucket in recording_buckets:
        recording_id = recording_bucket['key']
        total = recording_bucket['doc_count']
        recordings.append({'recording': recording_id, 'total': total})
    total_hits = es_result['hits']['total']
    return {'recordings': recordings, 'total': total_hits}


def _paginate_aggregation(es_result, args, aggregation_name):
    """Paginate aggregated results."""
    # Get bucket pagination arguments
    page = args.get('page') or 1
    per_page = args.get('per_page') or 10

    show_buckets = es_result['aggregations'][aggregation_name]['buckets']

    # Assuming all possible buckets are returned, we'll now pull out the 'page'
    # that we want. Elasticsearch does not allow aggregation pagination as of
    # Elasticsearch 1.4.4, so we'll have to do the pagination in-memory.
    # See https://github.com/elasticsearch/elasticsearch/issues/4915
    start_index = (page - 1) * per_page
    end_index = page * per_page
    show_buckets = show_buckets[start_index: end_index]
    return show_buckets


def format_songs(es_result):
    """Return the formatted songs."""
    total = es_result['hits']['total']
    songs = es_result['hits']['hits']
    # Clean the elasticsearch ids from the songs
    clean_songs = []
    for song in songs:
        data = song['_source']
        clean_songs.append(data)
    return {'total': total, 'songs': clean_songs}
