import json
import os
import unittest

from mock import Mock, patch

from download_songs import download_songs
from tests.utils import mongo_clean

fixtures_dir = 'tests/fixtures'


class TestDownloadShows(unittest.TestCase):
    def _mock_json(self):
        """A mock json() response method."""
        # Load the response fixture
        fixture_path = os.path.join(fixtures_dir, 'gd_details_response.json')
        with open(fixture_path, 'r') as fin:
            fixture_json = json.loads(fin.read())
        return fixture_json

    @mongo_clean
    def test_download_songs(self):
        # Mock the response
        mock_response = Mock()
        mock_attrs = {
            'json.return_value': self._mock_json(),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('download_songs.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                download_songs()
