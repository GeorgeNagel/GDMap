from datetime import datetime
import os
import sys
import time


from mongoengine import connect

from gdmap.data_scraping.geocode_show_listings import geocoding_dict
from gdmap.data_scraping.utils import json_request, APIException
from gdmap.data_scraping.archive_api.download_shows import show_identifiers
from gdmap.models import Song
from gdmap.settings import MONGO_DATABASE_NAME, SONGS_DIRECTORY, MONGODB_HOST_NAME, logging


log = logging.getLogger(__name__)


base_url = 'https://archive.org/details'


# Establish the connection to the database
connect(MONGO_DATABASE_NAME, host=MONGODB_HOST_NAME)

# A mapping of dates to venues to latitudes and longitudes
geo_dict = geocoding_dict()


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

    # Sometimes show location is not available on the item level
    venue = ""
    if 'venue' in details_dict['metadata']:
        venue = details_dict['metadata']['venue'][0]
    location = ""
    if 'coverage' in details_dict['metadata']:
        location = details_dict['metadata']['coverage'][0]

    lat, lon = _concert_lat_lon(geo_dict, show_date_text, venue)
    if lat is None or lon is None:
        log.warning("Could not geocode: %s - %s." % (show_date_text, venue))
        return []

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
                    song_data = {
                        'show_id': show_id,
                        'filename': file_.strip('/'),
                        'album': album,
                        'sha1': file_dict['sha1'],
                        'title': file_dict['title'],
                        'track': int(file_dict['track']),
                        'date': show_date_text,
                        'location': location,
                        'venue': venue,
                        'latlon': "%s,%s" % (lat, lon)
                    }
                    song = Song(**song_data)
                    log.debug("Song data: %s" % song_data)
                    songs.append(song)
        except KeyError as e:
            log.warning("Bad data in %s%s: %s" % (show_id, file_, e))
    return songs


def _concert_lat_lon(geocoding_dict, date_iso, venue):
    """
    Get the lat and lon for a concert, given a date and venue.
    venue may be None.
    """
    if date_iso not in geocoding_dict:
        log.warning("Unable to geocode concert on date: %s" % date_iso)
        return None, None
    possible_venues = geocoding_dict[date_iso].keys()
    if len(possible_venues) > 1:
        # We weren't given a venue on a date with multiple venues.
        # We won't be able to geocode.
        if not venue:
            return None, None
        # Check the edit distance between the given venue and possible venues
        # To select the most likely match
        best_match_venue = min(possible_venues, key=lambda x: _levenshtein(x, venue))

    else:
        best_match_venue = possible_venues[0]
    lat = geocoding_dict[date_iso][best_match_venue]['lat']
    lon = geocoding_dict[date_iso][best_match_venue]['lon']
    return lat, lon


def _levenshtein(seq1, seq2):
    """
    Calculate the edit distance between two sequences.
    http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    """
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]  # noqa
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]


def download_songs(year, crawl_delay_seconds=1, max_errors=10, **kwargs):
    """Download song information for a given year and save to mongo."""
    show_ids = show_identifiers(year)
    errors = 0
    for id_ in show_ids:
        url = "%s/%s&output=json" % (base_url, id_)
        cached = False
        try:
            response_dict, cached = json_request(url)
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


def dump_songs_json(year):
    """Dump all of the songs in a given year to a JSON file."""
    if not os.path.exists(SONGS_DIRECTORY):
        os.makedirs(SONGS_DIRECTORY)
    songs_filename = os.path.join(SONGS_DIRECTORY, "%s.jl" % year)
    year_string = str(year)
    next_year_string = str(year+1)
    with open(songs_filename, 'w') as fout:
        for song in Song.objects(date__gte=year_string, date__lt=next_year_string):
            fout.write('%s\n' % song.to_json())

if __name__ == '__main__':
    Song.objects.delete()
    if len(sys.argv[1:]) > 0:
        # Get songs info from specific years
        years = [int(year) for year in sys.argv[1:]]
    else:
        # Get all songs
        years = range(1967, 1996)
    for year in years:
        print "Downloading songs for year: %s" % year
        download_songs(year)
        dump_songs_json(year)
