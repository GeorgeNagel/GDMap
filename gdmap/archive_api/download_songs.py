from datetime import datetime
import os
import sys
import time


from mongoengine import connect

from gdmap.archive_api.utils import cache, internetarchive_json_api, APIException
from gdmap.archive_api.download_shows import show_identifiers
from gdmap.models import Song
from gdmap.settings import MONGO_DATABASE_NAME, logging


log = logging.getLogger(__name__)


base_url = 'https://archive.org/details'


# Establish the connection to the database
connect(MONGO_DATABASE_NAME)


def songs_from_details(details_dict):
    """Returns a list of Song documents from a details dict."""

    # Get show-wide values
    show_id = details_dict['dir'].split('/items/')[-1]
    show_date_text = details_dict['metadata']['date'][0]
    try:
        show_date = datetime.strptime(show_date_text, '%Y-%m-%d').date()
        show_date_text = show_date.isoformat()
    except ValueError as e:
        log.warning("Invalid date: %s" % e)
        return []

    # Sometimes show location is not available on an item level
    show_location = None
    if 'coverage' in details_dict['metadata']:
        show_location = details_dict['metadata']['coverage'][0]

    songs = []
    for file_ in details_dict['files']:
        try:
            file_dict = details_dict['files'][file_]
            log.debug("FILE DICT (%s, %s): %s" % (
                show_id, file_, file_dict)
            )
            _, extension = os.path.splitext(file_)
            if extension in ['.mp3', '.flac', '.ogg', '.shn']:
                # This is a song file
                if file_dict['source'] == 'original':
                    # We only care about one set of files, so just
                    # index the original files
                    album = file_dict['album']
                    if not show_location:
                        # There was no item-wide location info
                        # album is in the format of "1984-05-06 - Silva Hall at the Hult Center"
                        show_location = album.split('-')[-1].strip()
                    song_data = {
                        'show_id': show_id,
                        'filename': file_.strip('/'),
                        'album': album,
                        'sha1': file_dict['sha1'],
                        'title': file_dict['title'],
                        'track': int(file_dict['track']),
                        'date': show_date_text,
                        'location': show_location
                    }
                    song = Song(**song_data)
                    log.debug("Song data: %s" % song_data)
                    songs.append(song)
        except KeyError as e:
            log.warning("Bad data in %s%s: %s" % (show_id, file_, e))
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
            log.error(e)
            errors += 1
            if errors > max_errors:
                raise Exception("Max Requests errors exceeded: %d" % errors)

        if not cached:
            # Don't hit their api too hard too fast
            time.sleep(crawl_delay_seconds)

if __name__ == '__main__':
    crawl_delay_seconds = int(sys.argv[1])
    download_songs(crawl_delay_seconds=crawl_delay_seconds)
