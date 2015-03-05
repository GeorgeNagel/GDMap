import json
import time

from gdmap.es_index import index_songs
from gdmap.models import Song
from gdmap.settings import logging
from gdmap.tests.utils import mongo_clean, APITestCase

log = logging.getLogger(__name__)


class SongsAPITestCase(APITestCase):
    def setUp(self):
        # Two songs from the same show
        self.test_song_1 = Song(sha1='abc123',
                                show_id='test_show_id',
                                filename='test_filename',
                                album='test album',
                                title='test_title',
                                track=1,
                                date='1980-01-02',
                                location='New York, NY')

        # A song from another show
        self.test_song_2 = Song(sha1='abc1232',
                                show_id='test_show_id_2',
                                filename='test_filename_2',
                                album='test album_2',
                                title='test_title_2',
                                track=2,
                                date='1990-01-01',
                                location='Bingo, NY')
        super(SongsAPITestCase, self).setUp()

    @mongo_clean
    def test_query_all(self):
        """Test the results of querying for all songs."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        self.test_song_1.save()
        self.assertEqual(Song.objects.count(), 1)
        log.debug("Indexing test song.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        response = self.app.get('/api/songs/')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'album': u'test album',
                        u'date': u'1980-01-02',
                        u'filename': u'test_filename',
                        u'location': u'New York, NY',
                        u'show_id': u'test_show_id',
                        u'title': u'test_title',
                        u'track': 1
                    },
                ],
                u'total': 1
            }
        )

    @mongo_clean
    def test_sort(self):
        """Test sorting the songs."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        # Save songs from show 1
        self.test_song_1.save()
        # Save songs from show 2
        self.test_song_2.save()
        self.assertEqual(Song.objects.count(), 2)

        log.debug("Indexing test songs.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        # Query for every song with 'test' in the title or elsewhere
        response = self.app.get('/api/songs/?sort=date&sort_order=desc')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'album': u'test album_2',
                        u'date': u'1990-01-01',
                        u'filename': u'test_filename_2',
                        u'location': u'Bingo, NY',
                        u'show_id': u'test_show_id_2',
                        u'title': u'test_title_2',
                        u'track': 2
                    },
                    {
                        u'album': u'test album',
                        u'date': u'1980-01-02',
                        u'filename': u'test_filename',
                        u'location': u'New York, NY',
                        u'show_id': u'test_show_id',
                        u'title': u'test_title',
                        u'track': 1
                    }
                ],
                u'total': 2
            }
        )

    @mongo_clean
    def test_pagination(self):
        """Test paginating the songs."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        # Save songs from show 1
        self.test_song_1.save()
        # Save songs from show 2
        self.test_song_2.save()
        self.assertEqual(Song.objects.count(), 2)

        log.debug("Indexing test songs.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        # Query for every song with 'test' in the title or elsewhere
        response = self.app.get('/api/songs/?sort=date&sort_order=asc&page=2&per_page=1')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'album': u'test album_2',
                        u'date': u'1990-01-01',
                        u'filename': u'test_filename_2',
                        u'location': u'Bingo, NY',
                        u'show_id': u'test_show_id_2',
                        u'title': u'test_title_2',
                        u'track': 2
                    }
                ],
                u'total': 2
            }
        )

    @mongo_clean
    def test_album_search(self):
        """Test paginating the songs."""
        self.maxDiff = None
        log.debug("Saving song in Mongo.")
        # Save songs from show 1
        self.test_song_1.save()
        # Save songs from show 2
        self.test_song_2.save()
        self.assertEqual(Song.objects.count(), 2)

        log.debug("Indexing test songs.")
        index_songs()
        # Wait for the song to be indexed
        time.sleep(2)
        log.debug("Getting all indexed songs.")
        # Query for every song with 'test' in the title or elsewhere
        response = self.app.get('/api/songs/?album=test album_2')
        self.assertEqual(
            json.loads(response.data),
            {
                u'songs': [
                    {
                        u'album': u'test album_2',
                        u'date': u'1990-01-01',
                        u'filename': u'test_filename_2',
                        u'location': u'Bingo, NY',
                        u'show_id': u'test_show_id_2',
                        u'title': u'test_title_2',
                        u'track': 2
                    }
                ],
                u'total': 1
            }
        )

    def test_400_invalid_sort(self):
        response = self.app.get('/api/songs/?sort=toast')
        self.assertEqual(response.status, '400 BAD REQUEST')
