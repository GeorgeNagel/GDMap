import json
import os

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from gdmap.settings import ELASTICSEARCH_INDEX_NAME, DATA_DIRECTORY, logging

log = logging.getLogger(__name__)

es = Elasticsearch()

SONG_MAPPINGS = {
    "mappings": {
        "song": {
            "properties": {
                "sha1": {"type": "string", "index": "not_analyzed"},
                "show_id": {"type": "string", "index": "not_analyzed"},
                "filename": {"type": "string", "index": "not_analyzed"},
                "album": {
                    "type": "multi_field",
                    "fields": {
                        "album": {
                            "type": "string",
                            "index": "analyzed"
                        },
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "title": {"type": "string", "index": "analyzed"},
                "track": {"type": "integer"},
                # Let Elasticsearch take care of the date mapping for us
                "location": {"type": "string", "index": "analyzed"},
                "venue": {"type": "string", "index": "analyzed"},
                "latlon": {"type": "geo_point", "lat_lon": True}

            }
        }
    }
}


def recreate_index():
    # Delete the entire index
    if es.indices.exists(ELASTICSEARCH_INDEX_NAME):
        log.info("Removing index: %s" % ELASTICSEARCH_INDEX_NAME)
        # We use delete rather than flush in case the mapping has changed.
        es.indices.delete(ELASTICSEARCH_INDEX_NAME)
    es.indices.create(ELASTICSEARCH_INDEX_NAME, SONG_MAPPINGS)


def batch_index_songs(song_dicts):
    # Create the iterable of index actions for consumption by bulk()
    actions = [
        {
            '_id': song_dict['_id'],
            '_index': ELASTICSEARCH_INDEX_NAME,
            '_type': 'song',
            '_source': song_dict
        } for song_dict in song_dicts
    ]
    bulk(es, actions)
    log.debug(
        'Indexed song: %s%s' % (
            song_dict['show_id'],
            song_dict['filename']
        )
    )


def index_songs(year):
    """Index all of the songs into elasticsearch from data in .jl files."""
    print "Indexing songs for year: %s" % year
    songs_jl = os.path.join(DATA_DIRECTORY, 'songs/%s.jl' % year)
    # Read the songs in from file
    songs = []
    with open(songs_jl, 'r') as fin:
        for song in fin:
            song_dict = json.loads(song)
            songs.append(song_dict)
    # Batch index the songs into Elasticsearch
    batch_index_songs(songs)


def query_es(query_body):
    """Query the elasticsearch index."""
    res = es.search(index=ELASTICSEARCH_INDEX_NAME, body=query_body)
    return res

if __name__ == "__main__":
    recreate_index()
    years = range(1967, 1996)
    for year in years:
        index_songs(year)
