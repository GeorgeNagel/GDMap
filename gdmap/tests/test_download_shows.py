import json
import os
import unittest

from mock import Mock, patch, mock_open, call

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
        m_open = mock_open()
        # Patch the request to return the mocked response
        with patch('gdmap.data_scraping.utils.requests.get') as get_mock:
            get_mock.return_value = mock_response
            # Mock out the file open so that we don't actually write/overwrite the csv
            with patch('gdmap.data_scraping.archive_api.download_shows.open', m_open, create=True):
                download_shows(stop=1)
                # Check the file write
                self.assertEqual(
                    m_open.mock_calls,
                    [
                        call('/home/vagrant/gdmap/data/shows.csv', 'w'),
                        call().__enter__(),
                        call().write('show_id,date\r\n'),
                        call().write('gd1986-03-28.nak300.morris.crazyfingers.106564.flac16,1986-03-28T00:00:00Z\r\n'),
                        call().write('gd1984-06-27.senn.hubbard.bandrofcheck.81509.sbefail.flac16,1984-06-27T00:00:00Z\r\n'),  # noqa
                        call().write('gd1990-03-26.AKG451.Berger.Currier.Keo.120942.Flac2496,1990-03-26T00:00:00Z\r\n'),
                        call().write('gd1986-03-31.fob.thompson.motb.83475.flac24,1986-03-31T00:00:00Z\r\n'),
                        call().write('gd1992-06-11.nak300.baker-keo.sirmick.110979.sbeok.flac16,1992-06-11T00:00:00Z\r\n'),  # noqa
                        call().write('gd1987-06-19.nak300.barfield-lane.watson.104894.flac16,1987-06-19T00:00:00Z\r\n'),
                        call().write('gd1994-09-29.fob.schoeps.crow-cubby.sobel.96403.flac1648,1994-09-29T00:00:00Z\r\n'),  # noqa
                        call().write('gd1984-06-24.nak300.friend.109483.flac2448,1984-06-24T00:00:00Z\r\n'),
                        call().write('gd1989-04-16.AKG451.Darby.118403.Flac1644,1989-04-16T00:00:00Z\r\n'),
                        call().write('gd1984-10-11.nak300.morris.crazyfingers.106646.flac16,1984-10-11T00:00:00Z\r\n'),
                        call().__exit__(None, None, None)
                    ]
                )
