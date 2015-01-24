from unittest import TestCase

from gdmap.views.search_api.songs import _build_multi_field_query, \
    _build_match_query, _build_query_body


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
