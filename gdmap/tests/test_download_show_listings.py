import os
import unittest

from mock import Mock

from gdmap.data_scraping.dead_net.download_show_listings import parse_show_page
from gdmap.settings import TEST_FIXTURES_DIR


class ParseShowPageTestCase(unittest.TestCase):
    def _mock_response_from_fixture(self, fixture_name):
        mock_response = Mock()
        html_fixture_path = os.path.join(TEST_FIXTURES_DIR, fixture_name)
        with open(html_fixture_path, 'r') as fin:
            html_fixture = fin.read()
        mock_attrs = {
            'text': html_fixture,
        }
        mock_response.configure_mock(**mock_attrs)
        return mock_response

    def test_download_songs(self):
        mock_response = self._mock_response_from_fixture('dead_net_may_05_1965.html')
        parsed_page_info = parse_show_page(mock_response)
        self.assertEqual(
            parsed_page_info,
            {
                'date': u'May 05, 1965',
                'location': u'Menlo Park, CA US',
                'next': u'/show/may-12-1965',
                'venue': u"Magoo's Pizza Parlor"
            }
        )

    def test_non_link_location(self):
        """Test parsing a page that doesn't have a link to a location page."""
        mock_response = self._mock_response_from_fixture('dead_net_july_29_1966.html')
        parsed_page_info = parse_show_page(mock_response)
        self.assertEqual(
            parsed_page_info,
            {
                'date': u'July 29, 1966',
                'location': u'B.C., CA',
                'next': u'/show/july-30-1966',
                'venue': u"P.N.E. Garden Auditorium"
            }
        )

    def test_no_next_page(self):
        mock_response = self._mock_response_from_fixture('dead_net_february_24_1968.html')
        parsed_page_info = parse_show_page(mock_response)
        self.assertEqual(
            parsed_page_info,
            {
                'date': u'February 24, 1968',
                'location': u'Lake Tahoe, CA US',
                'next': None,
                'venue': u"King's Beach Bowl"
            }
        )
