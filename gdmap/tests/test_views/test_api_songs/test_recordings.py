import json
import time

from gdmap.es_index import index_songs
from gdmap.models import Song
from gdmap.settings import logging
from gdmap.tests.utils import mongo_clean, APITestCase

log = logging.getLogger(__name__)


class SongsAPITestCase(APITestCase):
    def setUp(self):
        # Two songs from the same concert, different recordings
        self.test_song_1 = Song(sha1='abc123',
                                show_id='test_show_id_1',
                                filename='test_filename_1',
                                album='test album 1',
                                title='test_title_1',
                                track=1,
                                date='1980-01-02',
                                location='New York, NY')

        self.test_song_2 = Song(sha1='abc1234',
                                show_id='test_show_id_2',
                                filename='test_filename_2',
                                album='test album 1',
                                title='test_title_2',
                                track=2,
                                date='1980-01-02',
                                location='New York, NY')

        # A song from another concert
        self.test_song_3 = Song(sha1='abc12345',
                                show_id='test_show_id_3',
                                filename='test_filename_3',
                                album='test album 2',
                                title='test_title_3',
                                track=2,
                                date='1990-01-01',
                                location='Bingo, NY')
        super(SongsAPITestCase, self).setUp()

    @mongo_clean
    def test_query_recordings(self):
        """Test the results of querying for all recordings."""
        self.maxDiff = None
        log.debug("Saving songs in Mongo.")
        self.test_song_1.save()
        self.test_song_2.save()
        self.test_song_3.save()
        self.assertEqual(Song.objects.count(), 3)
        log.debug("Indexing test song.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all recordings.")
        response = self.app.get('/api/recordings/')
        self.assertEqual(
            json.loads(response.data),
            {
                u'recordings': [
                    {
                        u'album': u'test album 2',
                        u'date': u'1990-01-01',
                        u'location': u'Bingo, NY',
                        u'show_id': u'test_show_id_3',
                        u'total': 1
                    },
                    {
                        u'album': u'test album 1',
                        u'date': u'1980-01-02',
                        u'location': u'New York, NY',
                        u'show_id': u'test_show_id_1',
                        u'total': 1
                    },
                    {
                        u'album': u'test album 1',
                        u'date': u'1980-01-02',
                        u'location': u'New York, NY',
                        u'show_id': u'test_show_id_2',
                        u'total': 1
                    }
                ],
                u'total': 3
            }
        )
