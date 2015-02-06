import json
import time
from unittest import TestCase

from gdmap.es_index import index_songs
from gdmap.models import Song
from gdmap.settings import logging
from gdmap.tests.utils import mongo_clean, APITestCase
from gdmap.views.search_api.songs import _build_multi_field_query, \
    _build_match_query, _build_query_body, _build_date_filter

log = logging.getLogger(__name__)

test_song = Song(sha1='abc123',
                 show_id='test_show_id',
                 filename='test_filename',
                 album='test_album',
                 title='test_title',
                 track=1,
                 date='1980-01-02',
                 location='New York, NY')


class SongsAPITestCase(APITestCase):
    @mongo_clean
    def test_query_all(self):
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        test_song.save()
        self.assertEqual(Song.objects.count(), 1)
        log.debug("Indexing test song.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        response = self.app.get('/api/songs/')
        self.assertEqual(
            json.loads(response.data),
            {
                "songs": [
                    {
                        "album": "test_album",
                        "date": "1980-01-02",
                        "filename": "test_filename",
                        "location": "New York, NY",
                        "show_id": "test_show_id",
                        "title": "test_title",
                        "track": 1
                    }
                ],
                "total": 1
            }
        )


class BuildQueryBodyTestCase(TestCase):
    def test_page_info_only(self):
        """No parameters (other than page info) should give a match_all query."""
        args = {'page': 2, 'per_page': 5}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'from': 5,
                'size': 5,
                'query': {
                    'match_all': {}
                }
            }
        )

    def test_multi_field_query(self):
        args = {'q': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'from': 0,
                'size': 10,
                'query': {
                    'multi_match': {
                        'fields': [
                            'sha1', 'show_id', 'filename',
                            'album', 'title', 'location'
                        ],
                        'query': 'miss'
                    }
                }
            }
        )

    def test_single_match_query(self):
        args = {'track': 4}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'from': 0,
                'size': 10,
                'query': {
                    'bool': {
                        'must': [{
                            'match': {
                                'track': 4
                            }
                        }]
                    }
                }
            }
        )

    def test_multiple_match_query(self):
        args = {'track': 4, 'title': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'from': 0,
                'size': 10,
                'query': {
                    'bool': {
                        'must': [
                            {
                                'match': {
                                    'title': 'miss'
                                }
                            },
                            {
                                'match': {
                                    'track': 4
                                }
                            }
                        ]
                    }
                }
            }
        )

    def test_date_filters_query(self):
        args = {'date_gte': "1990", 'date_lte': '1995-01-02'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'from': 0,
                'query': {
                    'filtered': {
                        'filter': {
                            'range': {
                                'date': {'gte': '1990', 'lte': '1995-01-02'}
                            }
                        },
                        'query': {'match_all': {}}
                    }
                },
                'size': 10
            }
        )

    def combined_query(self):
        """Test the case of a multifield query and targeted query."""
        args = {'q': 'diplo', 'track': 4, 'title': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'from': 0,
                'size': 10,
                'query': {
                    'bool': {
                        'must': [
                            {
                                'match': {
                                    'title': 'miss'
                                }
                            },
                            {
                                'match': {
                                    'track': 4
                                }
                            },
                            {
                                'multi_match': {
                                    'fields': [
                                        'sha1', 'show_id', 'filename',
                                        'album', 'title', 'location'
                                    ],
                                    'query': 'miss'
                                }
                            }
                        ]
                    }
                }
            }
        )


class BuildMultiFieldQueryTestCase(TestCase):
    def test_build_multi_field_query(self):
        phrase = "miss"
        query_body = _build_multi_field_query(phrase)
        self.assertEqual(
            query_body,
            {
                'multi_match': {
                    'fields': [
                        'sha1', 'show_id', 'filename',
                        'album', 'title', 'location'
                    ],
                    'query': 'miss'
                }
            }
        )


class BuildMatchQueryTestCase(TestCase):
    def test_build_match_query(self):
        field = 'track'
        value = 2
        query_body = _build_match_query(field, value)
        self.assertEqual(
            query_body,
            {'match': {'track': 2}}
        )


class BuildDateFilterTestCase(TestCase):
    def test_build_date_filter(self):
        filter_body = _build_date_filter("1990-01-02", "1990-01-03")
        self.assertEqual(
            filter_body,
            {
                "range": {
                    "date": {
                        "gte": "1990-01-02",
                        "lte": "1990-01-03"
                    }
                }
            }
        )
