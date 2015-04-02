import json
import time

from gdmap.es_index import index_songs
from gdmap.settings import logging
from gdmap.tests.utils import index_clean, APITestCase

log = logging.getLogger(__name__)


class SongsAPITestCase(APITestCase):
    @index_clean
    def test_query_all(self):
        """Test the results of querying for all songs."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        response = self.app.get('/api/songs/')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'_id': u'4ebd25dad72908f3fa370d9b9ea29fb6d82f9e1b',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t04.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'We Can Run',
                        u'track': 4,
                        u'venue': u'Civic Center'
                    },
                    {
                        u'_id': u'917c5b38b870625994a003ca2beed5e4ab45f5f4',
                        u'album': u'1990-03-25 - Knickerbocker Arena',
                        u'date': u'1990-03-25',
                        u'filename': u'gd90-03-25MTd2t03.shn',
                        u'latlon': u'42.6525793,-73.7562317',
                        u'location': u'Albany, NY',
                        u'show_id': u'gd1990-03-25.sbd.hollister.7508.shnf',
                        u'title': u'Crazy Fingers',
                        u'track': 11,
                        u'venue': u'Knickerbocker Arena'
                    },
                    {
                        u'_id': u'fdee660848cd1a28e6520f1b19760b2050194301',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t02.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'Hell in a Bucket',
                        u'track': 2,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 3
            }
        )

    @index_clean
    def test_sort(self):
        """Test sorting the songs."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        response = self.app.get('/api/songs/?sort=date&sort_order=desc')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'_id': u'917c5b38b870625994a003ca2beed5e4ab45f5f4',
                        u'album': u'1990-03-25 - Knickerbocker Arena',
                        u'date': u'1990-03-25',
                        u'filename': u'gd90-03-25MTd2t03.shn',
                        u'latlon': u'42.6525793,-73.7562317',
                        u'location': u'Albany, NY',
                        u'show_id': u'gd1990-03-25.sbd.hollister.7508.shnf',
                        u'title': u'Crazy Fingers',
                        u'track': 11,
                        u'venue': u'Knickerbocker Arena'
                    },
                    {
                        u'_id': u'4ebd25dad72908f3fa370d9b9ea29fb6d82f9e1b',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t04.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'We Can Run',
                        u'track': 4,
                        u'venue': u'Civic Center'
                    },
                    {
                        u'_id': u'fdee660848cd1a28e6520f1b19760b2050194301',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t02.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'Hell in a Bucket',
                        u'track': 2,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 3
            }
        )

    @index_clean
    def test_pagination(self):
        """Test paginating the songs."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        response = self.app.get('/api/songs/?sort=date&sort_order=asc&page=2&per_page=1')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'_id': u'fdee660848cd1a28e6520f1b19760b2050194301',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t02.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'Hell in a Bucket',
                        u'track': 2,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 3
            }
        )

    @index_clean
    def test_album_search(self):
        """Test paginating the songs."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        # Query for every song with 'test' in the title or elsewhere
        response = self.app.get('/api/songs/?album=1990-03-19 - Civic Center')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'_id': u'4ebd25dad72908f3fa370d9b9ea29fb6d82f9e1b',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t04.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'We Can Run',
                        u'track': 4,
                        u'venue': u'Civic Center'
                    },
                    {
                        u'_id': u'fdee660848cd1a28e6520f1b19760b2050194301',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t02.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'Hell in a Bucket',
                        u'track': 2,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 2
            }
        )

    @index_clean
    def test_and_terms(self):
        """Multiple search terms should further restrict results."""
        self.maxDiff = None
        index_songs(1990)
        # Wait for the song to be indexed
        time.sleep(2)
        response = self.app.get('/api/songs/?q=Civic Run')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'_id': u'4ebd25dad72908f3fa370d9b9ea29fb6d82f9e1b',
                        u'album': u'1990-03-19 - Civic Center',
                        u'date': u'1990-03-19',
                        u'filename': u'gd1990-03-19d1t04.flac',
                        u'latlon': u'41.7654588,-72.67215399999999',
                        u'location': u'Hartford , CT',
                        u'show_id': u'gd1990-03-19.nak300.carpenter.andrewf.86825.sbeok.flac16',
                        u'title': u'We Can Run',
                        u'track': 4,
                        u'venue': u'Civic Center'
                    }
                ],
                u'total': 1
            }
        )

    def test_400_invalid_sort(self):
        response = self.app.get('/api/songs/?sort=toast')
        self.assertEqual(response.status, '400 BAD REQUEST')
