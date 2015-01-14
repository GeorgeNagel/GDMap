import json
import os
import unittest

from mock import Mock, patch

from download_shows import internetarchive_search

fixtures_dir = 'tests/fixtures'


class TestDownloadShows(unittest.TestCase):
    def _mock_json(self):
        """A mock json() response method."""
        # Load the response fixture
        fixture_path = os.path.join(fixtures_dir, 'gd_search_response.json')
        with open(fixture_path, 'r') as fin:
            fixture_json = json.loads(fin.read())
        return fixture_json

    def test_download_shows(self):
        # Mock the response
        mock_response = Mock()
        mock_attrs = {
            'json.return_value': self._mock_json(),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('download_shows.requests.get') as get_mock:
            get_mock.return_value = mock_response

            docs = internetarchive_search(stop=1)
            self.assertEqual(len(docs), 10)
            self.assertEqual(
                docs[0]['collection'],
                [u'GratefulDead', u'etree']
            )
