import json
import time

from gdmap.es_index import index_songs
from gdmap.settings import logging
from gdmap.tests.utils import index_clean, APITestCase

log = logging.getLogger(__name__)


class RecordingsAPITestCase(APITestCase):
    @index_clean
    def test_query_recordings(self):
        """Test the results of querying for all recordings."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        response = self.app.get('/api/recordings/')
        self.assertEqual(
            json.loads(response.data),
            {
                u'recordings': [
                    {
                        u'_id': u'917c5b38b870625994a003ca2beed5e4ab45f5f4',
                        u'album': u'1990-03-25 - Knickerbocker Arena',
                        u'date': u'1990-03-25',
                        u'latlon': u'42.6525793,-73.7562317',
                        u'location': u'Albany, NY',
                        u'show_id': u'gd1990-03-25.sbd.hollister.7508.shnf',
                        u'total': 1,
                        u'venue': u'Knickerbocker Arena'
                    },
                    {
                        u'_id': u'4ebd25dad72908f3fa370d9b9ea29fb6d82f9e1b',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'total': 2,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 3
            }
        )

    @index_clean
    def test_query_recording_id(self):
        """Test querying and filtering on a recording id."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        response = self.app.get('/api/recordings/?show_id=gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16')
        self.assertEqual(
            json.loads(response.data),
            {
                u'recordings': [
                    {
                        u'_id': u'4ebd25dad72908f3fa370d9b9ea29fb6d82f9e1b',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'total': 2,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 2
            }
        )
