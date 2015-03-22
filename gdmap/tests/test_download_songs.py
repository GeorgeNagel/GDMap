import json
import os
import unittest

from mock import Mock, patch

from gdmap.data_scraping.archive_api.download_songs import download_songs, _concert_lat_lon
from gdmap.models import Song
from gdmap.settings import TEST_FIXTURES_DIR
from gdmap.tests.utils import mongo_clean


class TestDownloadSongs(unittest.TestCase):
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
        with patch('gdmap.data_scraping.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.data_scraping.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                self.assertEqual(Song.objects.count(), 0)

                download_songs(1990)

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
                        'date': '1990-07-18',
                        'location': 'Noblesville, IN',
                        'venue': 'Deer Creek Music Center',
                        "album": "1990-07-18 - Deer Creek Music Center",
                        "title": "Help On The Way",
                        "track": 1,
                        'latlon': "40.0455917,-86.0085955"
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
        with patch('gdmap.data_scraping.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.data_scraping.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                self.assertEqual(Song.objects.count(), 0)

                download_songs(1984)

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
                        'date': '1984-05-06',
                        "album": "1984-05-06 - Silva Hall at the Hult Center",
                        "title": "// Uncle John's Band >",
                        "venue": "",
                        "location": "",
                        "track": 1,
                        'latlon': "44.0520691,-123.0867536"
                    }
                )

    @mongo_clean
    def test_invalid_date(self):
        """Test creating songs from a details response with no coverage field."""
        self.maxDiff = None
        # Mock the response
        mock_response = Mock()
        json_fixture_path = os.path.join(TEST_FIXTURES_DIR, 'gd_details_response_invalid_date.json')
        mock_attrs = {
            'json.return_value': self._mock_json(json_fixture_path),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('gdmap.data_scraping.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.data_scraping.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                download_songs(1990)

                self.assertEqual(Song.objects.count(), 0)

    @mongo_clean
    def test_uknown_date(self):
        """Test downloading a song with a date not found on dead.net."""
        self.maxDiff = None
        # Mock the response
        mock_response = Mock()
        json_fixture_path = os.path.join(TEST_FIXTURES_DIR, 'gd_details_response_unknown_date.json')
        mock_attrs = {
            'json.return_value': self._mock_json(json_fixture_path),
            'status_code': 200
        }
        mock_response.configure_mock(**mock_attrs)
        # Patch the request to return the mocked response
        with patch('gdmap.data_scraping.utils.requests.get') as get_mock:
            # Patch show_identifiers() to return an id without making calls
            with patch('gdmap.data_scraping.archive_api.download_songs.show_identifiers') as ids_mock:
                ids_mock.return_value = ['abc123']
                get_mock.return_value = mock_response

                download_songs(1990)

                self.assertEqual(Song.objects.count(), 0)


class TestConcertLatLon(unittest.TestCase):
    def setUp(self):
        self.geocoding_dict = {
            '1990-01-01': {
                'Brixton Academy': {'lat': 5.0, 'lon': 6.1},
                'Alley Palley': {'lat': -1.4, 'lon': 12.5}
            }
        }

    def test_concert_lat_lon(self):
        lat, lon = _concert_lat_lon(self.geocoding_dict, '1990-01-01', 'Academy')
        self.assertEqual(lat, 5.0)
        self.assertEqual(lon, 6.1)

        lat, lon = _concert_lat_lon(self.geocoding_dict, '1990-01-01', 'alley pal')
        self.assertEqual(lat, -1.4)
        self.assertEqual(lon, 12.5)

    def test_unknown_date(self):
        lat, lon = _concert_lat_lon(self.geocoding_dict, '1990-05-06', 'alley pal')
        self.assertEqual(lat, None)
        self.assertEqual(lon, None)
