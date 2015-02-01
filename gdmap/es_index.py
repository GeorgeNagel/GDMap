import json

from elasticsearch import Elasticsearch, ConnectionTimeout

from gdmap.models import Song
from gdmap.settings import ELASTICSEARCH_INDEX_NAME, logging

log = logging.getLogger(__name__)

es = Elasticsearch()
doc_type = 'song'


def index_song(song_document):
    song_data = json.loads(song_document.to_json())
    song_data.pop('_id')
    index_attempts = 0
    while index_attempts < 3:
        try:
            es.create(index=ELASTICSEARCH_INDEX_NAME,
                      doc_type=doc_type,
                      body=song_data,
                      timeout=100)
            # It worked without raising an exception
            break
        except ConnectionTimeout:
            log.warning(
                "Connection timeout. Retrying (%d)" % (index_attempts+1)
            )
            index_attempts += 1
    log.debug(
        'Indexed song: %s%s' % (
            song_data['show_id'],
            song_data['filename']
        )
    )


def index_songs():
    """Index all of the songs into elasticsearch from data in mongo."""
    # Delete the entire index
    if es.indices.exists(ELASTICSEARCH_INDEX_NAME):
        log.info("Removing index: %s" % ELASTICSEARCH_INDEX_NAME)
        # We use delete rather than flush in case the mapping has changed.
        es.indices.delete(ELASTICSEARCH_INDEX_NAME)
    for song in Song.objects:
        index_song(song)


def query_es(query_body):
    """Query the elasticsearch index."""
    res = es.search(index=ELASTICSEARCH_INDEX_NAME, body=query_body)
    return res

if __name__ == "__main__":
    index_songs()
