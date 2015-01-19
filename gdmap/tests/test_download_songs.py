import json
import os
import unittest

from mock import Mock, patch

from gdmap.archive_api.download_songs import download_songs
from gdmap.models import Song
from gdmap.tests.utils import mongo_clean

fixtures_dir = 'gdmap/tests/fixtures'


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
        with patch('gdmap.archive_api.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                num_songs = Song.objects.count()
                self.assertEqual(num_songs, 0)

                download_songs()

                num_songs = Song.objects.count()
                self.assertEqual(num_songs, 19)

                # Inspect a song object for correct data
                song = Song.objects(sha1="a00830c80d1cad6279de17ddfac78c772686db4a").first()
                song_data = json.loads(song.to_json())
                self.assertEqual(
                    song_data,
                    {
                        "_id": "a00830c80d1cad6279de17ddfac78c772686db4a",
                        "show_id": "gd90-07-18.neumann-fob.gardner.7358.sbeok.shnf",
                        "filename": "gd90-07-18d1t01.shn",
                        "album": "1990-07-18 - Deer Creek Music Center",
                        "title": "Help On The Way",
                        "track": 1
                    }
                )
