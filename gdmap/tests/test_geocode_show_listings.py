from unittest import TestCase

from gdmap.data_scraping.geocode_show_listings import geocoding_dict


class TestGeocodingDict(TestCase):
    def test_geocoding_dict(self):
        geo_dict = geocoding_dict()
        self.assertIn('1967-04-09', geo_dict)
        self.assertEqual(
            geo_dict['1967-04-09'],
            {
                "Longshoreman's Hall": {'lat': '37.7749295', 'lon': '-122.4194155'},
                'Panhandle': {'lat': '37.7728515', 'lon': '-122.4460161'}
            }
        )
