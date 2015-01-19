import logging
import os
import time


from mongoengine import connect

from archive_api.utils import cache, internetarchive_json_api, APIException
from download_shows import show_identifiers
from models import Song
from settings import MONGO_DATABASE_NAME


logging.basicConfig(level=logging.INFO)


base_url = 'https://archive.org/details'


# Establish the connection to the database
connect(MONGO_DATABASE_NAME)


def songs_from_details(details_dict):
    """Returns a list of Song documents from a details dict."""
    songs = []
    show_path = details_dict['dir']
    # Get the show id from the path
    show_id = show_path.split('/items/')[-1]
    for file_ in details_dict['files']:
        try:
            file_dict = details_dict['files'][file_]
            logging.debug("FILE DICT (%s, %s): %s" % (
                show_id, file_, file_dict)
            )
            _, extension = os.path.splitext(file_)
            if extension in ['.mp3', '.flac', '.ogg', '.shn']:
                # This is a song file
                if file_dict['source'] == 'original':
                    # We only care about one set of files, so just
                    # index the original files
                    song_data = {
                        'show_id': show_id,
                        'filename': file_.strip('/'),
                        'album': file_dict['album'],
                        'sha1': file_dict['sha1'],
                        'title': file_dict['title'],
                        'track': int(file_dict['track'])
                    }
                    song = Song(**song_data)
                    logging.debug("Song data: %s" % song_data)
                    songs.append(song)
        except KeyError as e:
            logging.warning("Bad data in %s%s: %s" % (show_id, file_, e))
    return songs


def download_songs(crawl_delay_seconds=1, max_errors=10, **kwargs):
    """Download song information and save to mongo."""
    show_ids = show_identifiers(from_file=True)
    errors = 0
    for id_ in show_ids:
        url = "%s/%s&output=json" % (base_url, id_)
        cached = cache.has_url(url)
        try:
            response_dict = internetarchive_json_api(url)
            songs = songs_from_details(response_dict)
            for song in songs:
                song.save()
        except APIException as e:
            logging.error(e)
            errors += 1
            if errors > max_errors:
                raise Exception("Max Requests errors exceeded: %d" % errors)

        if not cached:
            # Don't hit their api too hard too fast
            time.sleep(crawl_delay_seconds)

if __name__ == '__main__':
    download_songs()
