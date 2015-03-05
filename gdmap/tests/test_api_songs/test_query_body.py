from unittest import TestCase

from gdmap.views.search_api.songs_query_body import _build_query_body, \
    _build_multi_field_query, _build_match_query, _build_date_filter, \
    show_aggregations_body, build_songs_query


class BuildQueryBodyTestCase(TestCase):
    def test_sort_aggregation(self):
        """Test the query body when a sort order is specified."""
        self.maxDiff = None
        args = {'sort': 'date', 'sort_order': 'asc'}
        query_body = show_aggregations_body(args)
        self.assertEqual(
            query_body,
            {
                'shows': {
                    'aggregations': {
                        'shows_hits': {'top_hits': {'size': 1}},
                        "top_hit_score": {"max": {"script": "_score"}},
                        "top_hit_date": {"avg": {"field": "date"}}
                    },
                    'terms': {
                        'field': 'album.raw',
                        'size': 0,
                        'order': {'top_hit_date': 'asc'}
                    }
                }
            }
        )

    def test_multi_field_query(self):
        self.maxDiff = None
        args = {'q': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
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
        self.maxDiff = None
        args = {'track': 4}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
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
                'query': {
                    'filtered': {
                        'filter': {
                            'range': {
                                'date': {'gte': '1990', 'lte': '1995-01-02'}
                            }
                        },
                        'query': {'match_all': {}}
                    }
                }
            }
        )

    def test_combined_query(self):
        """Test the case of a multifield query and targeted query."""
        self.maxDiff = None
        args = {'q': 'diplo', 'track': 4, 'title': 'miss'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
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
                                    'query': 'diplo'
                                }
                            }
                        ]
                    }
                }
            }
        )

    def test_album_query(self):
        """Test querying for a specific album."""
        self.maxDiff = None
        args = {'album': '1970 Dingle Park'}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'query': {
                    'filtered': {
                        'filter': {
                            'term': {'album.raw': '1970 Dingle Park'}
                        },
                        'query': {'match_all': {}}
                    }
                }
            }
        )

    def test_multiple_filters(self):
        """Test when multiple filters are active."""
        self.maxDiff = None
        args = {'album': '1970 Dingle Park', 'date_gte': "1950"}
        query_body = _build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'query': {
                    'filtered': {
                        'filter': {
                            'and': [
                                {
                                    'range': {'date': {'gte': '1950'}}
                                },
                                {
                                    'term': {'album.raw': '1970 Dingle Park'}
                                }
                            ]
                        },
                        'query': {'match_all': {}}
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


class BuildSongsQueryTestCase(TestCase):
    def test_sort(self):
        self.maxDiff = None
        args = {'sort': 'date', 'sort_order': 'desc'}
        query_body = build_songs_query(args)
        self.assertEqual(
            query_body,
            {
                'from': 0,
                'size': 10,
                'query': {'match_all': {}},
                'sort': [{'date': {'order': 'desc'}}]
            }
        )

    def test_pagination(self):
        self.maxDiff = None
        args = {'page': 2, 'per_page': 5}
        query_body = build_songs_query(args)
        self.assertEqual(
            query_body,
            {'from': 5, 'query': {'match_all': {}}, 'size': 5}
        )
