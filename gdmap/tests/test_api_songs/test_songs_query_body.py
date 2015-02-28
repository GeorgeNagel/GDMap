from unittest import TestCase

from gdmap.views.search_api.songs_query_body import build_query_body, \
    _build_multi_field_query, _build_match_query, _build_date_filter


class BuildQueryBodyTestCase(TestCase):
    def test_page_info_only(self):
        """No parameters (other than page info) should give a match_all query."""
        self.maxDiff = None
        args = {'page': 2, 'per_page': 5}
        query_body = build_query_body(args)
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
                'size': 0,
                'query': {
                    'match_all': {}
                }
            }
        )

    def test_sort(self):
        """Test the query body when a sort order is specified."""
        self.maxDiff = None
        args = {'page': 2, 'per_page': 5, 'sort': 'title'}
        query_body = build_query_body(args)
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
                'size': 0,
                'query': {
                    'match_all': {}
                },
                "sort": [{"title": {"order": "asc"}}]
            }
        )

    def test_multi_field_query(self):
        self.maxDiff = None
        args = {'q': 'miss'}
        query_body = build_query_body(args)
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
                'size': 0,
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
        query_body = build_query_body(args)
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
                'size': 0,
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
        query_body = build_query_body(args)
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
                'size': 0,
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
        query_body = build_query_body(args)
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
                'size': 0
            }
        )

    def combined_query(self):
        """Test the case of a multifield query and targeted query."""
        self.maxDiff = None
        args = {'q': 'diplo', 'track': 4, 'title': 'miss'}
        query_body = build_query_body(args)
        self.assertEqual(
            query_body,
            {
                'size': 0,
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
