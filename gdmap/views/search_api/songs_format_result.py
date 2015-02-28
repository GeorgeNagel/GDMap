"""Utilities to format songs results from elasticsearch."""


def format_result(es_result):
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
