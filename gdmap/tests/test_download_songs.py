import json
import os
import unittest

from mock import Mock, patch

from gdmap.archive_api.download_songs import download_songs
from gdmap.models import Song
from gdmap.settings import TEST_FIXTURES_DIR
from gdmap.tests.utils import mongo_clean


class TestDownloadShows(unittest.TestCase):
    def _mock_json(self, json_fixture_path):
        """A mock json() response method."""
        # Load the response fixture
        with open(json_fixture_path, 'r') as fin:
            fixture_json = json.loads(fin.read())
        return fixture_json

    @mongo_clean
    def test_download_songs(self):
        self.maxDiff = None
        # Mock the response
        mock_response = Mock()
        json_fixture_path = os.path.join(TEST_FIXTURES_DIR, 'gd_details_response.json')
        mock_attrs = {
            'json.return_value': self._mock_json(json_fixture_path),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('gdmap.archive_api.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                self.assertEqual(Song.objects.count(), 0)

                download_songs()

                self.assertEqual(Song.objects.count(), 19)

                # Inspect a song object for correct data
                song = Song.objects(sha1="a00830c80d1cad6279de17ddfac78c772686db4a").first()
                song_data = json.loads(song.to_json())
                self.assertEqual(
                    song_data,
                    {
                        "_id": "a00830c80d1cad6279de17ddfac78c772686db4a",
                        "show_id": "gd90-07-18.neumann-fob.gardner.7358.sbeok.shnf",
                        "filename": "gd90-07-18d1t01.shn",
                        # Embedded document representation of datetime
                        'date': '1990-07-18T00:00:00',
                        'location': 'Noblesville, IN',
                        "album": "1990-07-18 - Deer Creek Music Center",
                        "title": "Help On The Way",
                        "track": 1
                    }
                )

    @mongo_clean
    def test_no_coverage(self):
        self.maxDiff = None
        """Test creating songs from a details response with no coverage field."""
        # Mock the response
        mock_response = Mock()
        json_fixture_path = os.path.join(TEST_FIXTURES_DIR, 'gd_details_response_no_coverage.json')
        mock_attrs = {
            'json.return_value': self._mock_json(json_fixture_path),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('gdmap.archive_api.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                self.assertEqual(Song.objects.count(), 0)

                download_songs()

                self.assertEqual(Song.objects.count(), 15)

                # Inspect a song object for correct data
                song = Song.objects(sha1="597c9fe1c781fb89e27b276e30331f66aa6f5c99").first()
                song_data = json.loads(song.to_json())
                self.assertEqual(
                    song_data,
                    {
                        "_id": "597c9fe1c781fb89e27b276e30331f66aa6f5c99",
                        "show_id": "gd1984-05-06.senn421-set2.unknown.29302.sbefail.flac16",
                        "filename": "gd1984-05-06set2d1t01.flac",
                        # Embedded document representation of datetime
                        'date': '1984-05-06T00:00:00',
                        'location': 'Silva Hall at the Hult Center',
                        "album": "1984-05-06 - Silva Hall at the Hult Center",
                        "title": "// Uncle John's Band >",
                        "track": 1
                    }
                )

    @mongo_clean
    def test_invalid_date(self):
        self.maxDiff = None
        """Test creating songs from a details response with no coverage field."""
        # Mock the response
        mock_response = Mock()
        json_fixture_path = os.path.join(TEST_FIXTURES_DIR, 'gd_details_response_invalid_date.json')
        mock_attrs = {
            'json.return_value': self._mock_json(json_fixture_path),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('gdmap.archive_api.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                download_songs()

                self.assertEqual(Song.objects.count(), 0)
