"""Utilities to format songs results from elasticsearch."""


def format_songs_by_show(es_result, args):
    """Return the formatted songs grouped by show."""
    # Get bucket pagination arguments
    total_buckets = len(es_result['aggregations']['shows']['buckets'])
    page = args.get('page') or 1
    per_page = args.get('per_page') or 10
    paginated_buckets = _paginate_aggregation(es_result, page, per_page, 'shows')

    songs_by_shows = []
    for show_bucket in paginated_buckets:
        show_name = show_bucket['key']
        songs = show_bucket['shows_hits']['hits']['hits']
        total = show_bucket['shows_hits']['hits']['total']
        # Clean the elasticsearch ids from the songs
        clean_songs = []
        for song in songs:
            clean_songs.append(song['_source'])
        songs_by_shows.append({'show': show_name, 'total': total, 'songs': clean_songs})
    formatted_result = {
        'songs_by_show': songs_by_shows,
        'total': total_buckets,
        'page': page,
        'per_page': per_page
    }
    return formatted_result


def format_recordings(es_result, args):
    """Return the formatted recording info."""
    # Get bucket pagination arguments
    page = args.get('page') or 1
    per_page = args.get('per_page') or 10
    recording_buckets = _paginate_aggregation(es_result, page, per_page, 'recordings')

    recordings = []
    for recording_bucket in recording_buckets:
        # Grab the relevant info from the first returned song for this bucket
        song = recording_bucket['recordings_hits']['hits']['hits'][0]
        song_info = song['_source']
        song_info.pop('title')
        song_info.pop('track')
        song_info.pop('filename')
        recording_info = song_info
        total = recording_bucket['recordings_hits']['hits']['total']
        recording_info['total'] = total
        recordings.append(recording_info)
    total_hits = es_result['hits']['total']
    return {'recordings': recordings, 'total': total_hits}


def _paginate_aggregation(es_result, page, per_page, aggregation_name):
    """Paginate aggregated results."""
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
