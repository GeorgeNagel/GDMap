import csv
import logging
import os
import sys
import time

from gdmap.data_scraping.utils import json_request, APIException
from gdmap.settings import DATA_DIRECTORY

logging.basicConfig(level=logging.INFO)

base_url = "https://archive.org/advancedsearch.php"
collection = "GratefulDead"
per_page = 100
crawl_delay_seconds = 1
start = 0

SHOWS_FILENAME = os.path.join(DATA_DIRECTORY, "shows.csv")


def download_shows(collection='GratefulDead',
                   per_page=100,
                   start=0,
                   crawl_delay_seconds=1,
                   max_errors=10,
                   stop=None):
    """Download show ids and save them in a csv, along with their date."""
    docs = []
    errors = 0
    while True:
        # Build the request
        query = "collection:(%s)&rows=%d&start=%d" % (
            collection, per_page, start)
        url = "%s?q=%s&output=json" % (base_url, query)

        try:
            # Get the search api response
            response_dict, cached = json_request(url)
            # Add the returned documents to the ongoing list
            requested_docs = response_dict['response']['docs']
            if not requested_docs:
                # You have gone past the last page of data
                break
            docs.extend(requested_docs)
        except APIException as e:
            logging.error(e)
            errors += 1
            if errors > max_errors:
                raise Exception("Max Requests errors exceeded: %d" % errors)

        # Increment the page for the next search
        start = start + per_page
        if not cached:
            # We did not just hit our cache, so be a good neighbor and sleep
            time.sleep(crawl_delay_seconds)
        # Exit after you have the item at index 'stop'
        if stop is not None and start >= stop:
            break

    # Write the csv file
    with open(SHOWS_FILENAME, 'w') as fout:
        csvwriter = csv.writer(fout)
        csvwriter.writerow(['identifier', 'date'])
        for doc in docs:
            # Some recordings don't have a date in the search result
            # Usually this is due to poorly formatted dates, like 1967-03-85
            date = doc.get('date', 'no-date')
            identifier = doc['identifier']
            csvwriter.writerow([identifier, date])


def show_identifiers(year):
    """Return a list of internetarchive show ids.
    Year is a number like 1990 or string, like '1999',
    or 'no-date' to match recordings that didn't provide a date.
    """
    # Cast any number years to strings
    year = str(year)

    # Load whatever ids are currently stored in file
    if os.path.exists(SHOWS_FILENAME):
        shows = []
        with open(SHOWS_FILENAME, 'r') as fin:
            csvreader = csv.DictReader(fin)
            for show_dict in csvreader:
                shows.append(show_dict)
        if not year:
            filtered_shows = [show for show in shows if not show['date']]
        else:
            filtered_shows = [show for show in shows if show['date'].startswith(year)]
        show_ids = [show['identifier'] for show in filtered_shows]
        return show_ids

    else:
        raise Exception("%s does not exist." % SHOWS_FILENAME)


if __name__ == '__main__':
    crawl_delay_seconds = int(sys.argv[1])
    download_shows(crawl_delay_seconds=crawl_delay_seconds)
