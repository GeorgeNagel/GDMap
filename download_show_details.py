import logging
import os
import time

import requests
import requests_cache
from mongoengine import connect

from download_shows import show_identifiers_from_file
from models import Song

from settings import MONGO_DATABASE_NAME


logging.basicConfig(level=logging.INFO)

# 1 month cache expiration
cache_expiration_seconds = 2419200
requests_cache.install_cache('cache',
                             backend='mongo',
                             expire_after=cache_expiration_seconds)
cache = requests_cache.core.get_cache()

base_url = 'https://archive.org/details'


# Establish the connection to the database
connect(MONGO_DATABASE_NAME)


class APIException(Exception):
    pass


def internetarchive_json_api(url):
    """Download details for an individual show."""
    # Get the details json response
    logging.info("Requesting: %s" % url)
    cached = cache.has_url(url)
    response = requests.get(url)
    response_dict = response.json()
    status = response.status_code
    logging.info("Response %d Cached? %s" % (status, cached))
    if status == 200:
        # Add the details to the ongoing collection
        return response_dict
    else:
        raise APIException("Error (%d) downloading: %s" % (status, url))


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


def download_show_details(crawl_delay_seconds=1, max_errors=10, **kwargs):
    show_ids = show_identifiers_from_file()
    details = []
    errors = 0
    for id_ in show_ids:
        url = "%s/%s&output=json" % (base_url, id_)
        cached = cache.has_url(url)
        try:
            response_dict = internetarchive_json_api(url, **kwargs)
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
    return details

if __name__ == '__main__':
    download_show_details()
