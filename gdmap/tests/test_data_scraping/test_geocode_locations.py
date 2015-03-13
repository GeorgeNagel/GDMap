import json
import os
import unittest

from mock import Mock, patch

from gdmap.data_scraping.archive_api.download_shows import download_shows
from gdmap.settings import TEST_FIXTURES_DIR


class TestDownloadShows(unittest.TestCase):
    def _mock_json(self):
        """A mock json() response method."""
        # Load the response fixture
        fixture_path = os.path.join(TEST_FIXTURES_DIR, 'gd_search_response.json')
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
        with patch('gdmap.data_scraping.utils.requests.get') as get_mock:
            get_mock.return_value = mock_response

            docs = download_shows(stop=1)
            self.assertEqual(len(docs), 10)
            self.assertEqual(
                docs[0]['collection'],
                [u'GratefulDead', u'etree']
            )
