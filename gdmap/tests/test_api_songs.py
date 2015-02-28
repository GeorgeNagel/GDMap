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


class SongsAPITestCase(APITestCase):
    def setUp(self):
        # Two songs from the same show
        self.test_song_1 = Song(sha1='abc123',
                                show_id='test_show_id',
                                filename='test_filename',
                                album='test album',
                                title='test_title',
                                track=1,
                                date='1980-01-02',
                                location='New York, NY')

        # A song from another show
        self.test_song_2 = Song(sha1='abc1232',
                                show_id='test_show_id_2',
                                filename='test_filename_2',
                                album='test album_2',
                                title='test_title_2',
                                track=2,
                                date='1990-01-01',
                                location='Bingo, NY')
        super(SongsAPITestCase, self).setUp()

    @mongo_clean
    def test_query_all(self):
        """Test the results of querying for all songs."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        self.test_song_1.save()
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
                'songs': {
                    "songs": [
                        {
                            "album": "test album",
                            "date": "1980-01-02",
                            "filename": "test_filename",
                            "location": "New York, NY",
                            "show_id": "test_show_id",
                            "title": "test_title",
                            "track": 1
                        }
                    ],
                    "total": 1
                },
                'songs_by_show': [
                    {
                        u'show': u'test album',
                        u'songs': [
                            {
                                u'album': u'test album',
                                u'date': u'1980-01-02',
                                u'filename': u'test_filename',
                                u'location': u'New York, NY',
                                u'show_id': u'test_show_id',
                                u'title': u'test_title',
                                u'track': 1
                            },
                        ],
                        u'total': 1}]}
        )

    @mongo_clean
    def test_shows_aggregation(self):
        """Test the show aggregation results for multiple songs."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        # Save songs from show 1
        self.test_song_1.save()
        # Save songs from show 2
        self.test_song_2.save()
        self.assertEqual(Song.objects.count(), 2)

        log.debug("Indexing test songs.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        # Query for every song with 'test' in the title or elsewhere
        response = self.app.get('/api/songs/?sort=title')
        self.assertEqual(
            json.loads(response.data),
            {
                'songs': {
                    u'songs': [
                        {
                            u'album': u'test album',
                            u'date': u'1980-01-02',
                            u'filename': u'test_filename',
                            u'location': u'New York, NY',
                            u'show_id': u'test_show_id',
                            u'title': u'test_title',
                            u'track': 1
                        },
                        {
                            u'album': u'test album_2',
                            u'date': u'1990-01-01',
                            u'filename': u'test_filename_2',
                            u'location': u'Bingo, NY',
                            u'show_id': u'test_show_id_2',
                            u'title': u'test_title_2',
                            u'track': 2
                        }
                    ],
                    u'total': 2
                },
                u'songs_by_show': [
                    {
                        u'show': u'test album_2',
                        u'songs': [
                            {
                                u'album': u'test album_2',
                                u'date': u'1990-01-01',
                                u'filename': u'test_filename_2',
                                u'location': u'Bingo, NY',
                                u'show_id': u'test_show_id_2',
                                u'title': u'test_title_2',
                                u'track': 2
                            }
                        ],
                        u'total': 1
                    },
                    {
                        u'show': u'test album',
                        u'songs': [
                            {
                                u'album': u'test album',
                                u'date': u'1980-01-02',
                                u'filename': u'test_filename',
                                u'location': u'New York, NY',
                                u'show_id': u'test_show_id',
                                u'title': u'test_title',
                                u'track': 1
                            }
                        ],
                        u'total': 1}
                ]
            }
        )

    @mongo_clean
    def test_aggregation_sort(self):
        """Test the aggregations are sorted by the top hit result."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        # Save songs from show 1
        self.test_song_1.save()
        # Save songs from show 2
        self.test_song_2.save()
        self.assertEqual(Song.objects.count(), 2)

        log.debug("Indexing test songs.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        # Query for every song with 'test' in the title or elsewhere
        response = self.app.get('/api/songs/?sort=title')
        self.assertEqual(
            json.loads(response.data),
            {
                'songs': {
                    u'songs': [
                        {
                            u'album': u'test album',
                            u'date': u'1980-01-02',
                            u'filename': u'test_filename',
                            u'location': u'New York, NY',
                            u'show_id': u'test_show_id',
                            u'title': u'test_title',
                            u'track': 1
                        },
                        {
                            u'album': u'test album_2',
                            u'date': u'1990-01-01',
                            u'filename': u'test_filename_2',
                            u'location': u'Bingo, NY',
                            u'show_id': u'test_show_id_2',
                            u'title': u'test_title_2',
                            u'track': 2
                        }
                    ],
                    u'total': 2
                },
                u'songs_by_show': [
                    {
                        u'show': u'test album_2',
                        u'songs': [
                            {
                                u'album': u'test album_2',
                                u'date': u'1990-01-01',
                                u'filename': u'test_filename_2',
                                u'location': u'Bingo, NY',
                                u'show_id': u'test_show_id_2',
                                u'title': u'test_title_2',
                                u'track': 2
                            }
                        ],
                        u'total': 1
                    },
                    {
                        u'show': u'test album',
                        u'songs': [
                            {
                                u'album': u'test album',
                                u'date': u'1980-01-02',
                                u'filename': u'test_filename',
                                u'location': u'New York, NY',
                                u'show_id': u'test_show_id',
                                u'title': u'test_title',
                                u'track': 1
                            }
                        ],
                        u'total': 1}
                ]
            }
        )

    def test_400_invalid_sort(self):
        response = self.app.get('/api/songs/?sort=toast')
        self.assertEqual(response.status, '400 BAD REQUEST')


class BuildQueryBodyTestCase(TestCase):
    def test_page_info_only(self):
        """No parameters (other than page info) should give a match_all query."""
        self.maxDiff = None
        args = {'page': 2, 'per_page': 5}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'aggregations': {
                    'shows': {
                        'aggregations': {
                            'shows_hits': {'top_hits': {'size': 1}},
                            "top_hit_score": {"max": {"script": "_score"}},
                            "top_hit_date": {"avg": {"field": "date"}}
                        },
                        'terms': {
                            'field': 'album.raw',
                            'size': 5,
                            'order': {'top_hit_score': 'desc'}
                        }
                    }
                },
                'from': 5,
                'size': 5,
                'query': {
                    'match_all': {}
                }
            }
        )

    def test_sort(self):
        """Test the query body when a sort order is specified."""
        self.maxDiff = None
        args = {'page': 2, 'per_page': 5, 'sort': 'title'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'aggregations': {
                    'shows': {
                        'aggregations': {
                            'shows_hits': {'top_hits': {'size': 1}},
                            "top_hit_score": {"max": {"script": "_score"}},
                            "top_hit_date": {"avg": {"field": "date"}}
                        },
                        'terms': {
                            'field': 'album.raw',
                            'size': 5,
                            'order': {'top_hit_score': 'desc'}
                        }
                    }
                },
                'from': 5,
                'size': 5,
                'query': {
                    'match_all': {}
                },
                "sort": [{"title": {"order": "asc"}}]
            }
        )

    def test_multi_field_query(self):
        self.maxDiff = None
        args = {'q': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'aggregations': {
                    'shows': {
                        'aggregations': {
                            'shows_hits': {'top_hits': {'size': 1}},
                            "top_hit_score": {"max": {"script": "_score"}},
                            "top_hit_date": {"avg": {"field": "date"}}
                        },
                        'terms': {
                            'field': 'album.raw',
                            'size': 10,
                            'order': {'top_hit_score': 'desc'}
                        }
                    }
                },
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
                'aggregations': {
                    'shows': {
                        'aggregations': {
                            'shows_hits': {'top_hits': {'size': 1}},
                            "top_hit_score": {"max": {"script": "_score"}},
                            "top_hit_date": {"avg": {"field": "date"}}
                        },
                        'terms': {
                            'field': 'album.raw',
                            'size': 10,
                            'order': {'top_hit_score': 'desc'}
                        }
                    }
                },
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
        """Test the query body for a multi-field query."""
        args = {'track': 4, 'title': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'aggregations': {
                    'shows': {
                        'aggregations': {
                            'shows_hits': {'top_hits': {'size': 1}},
                            "top_hit_score": {"max": {"script": "_score"}},
                            "top_hit_date": {"avg": {"field": "date"}}
                        },
                        'terms': {
                            'field': 'album.raw',
                            'size': 10,
                            'order': {'top_hit_score': 'desc'}
                        }
                    }
                },
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
        self.maxDiff = None
        args = {'date_gte': "1990", 'date_lte': '1995-01-02'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'aggregations': {
                    'shows': {
                        'aggregations': {
                            'shows_hits': {'top_hits': {'size': 1}},
                            "top_hit_score": {"max": {"script": "_score"}},
                            "top_hit_date": {"avg": {"field": "date"}}
                        },
                        'terms': {
                            'field': 'album.raw',
                            'size': 10,
                            'order': {'top_hit_score': 'desc'}
                        }
                    }
                },
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
        self.maxDiff = None
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
        self.maxDiff = None
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
