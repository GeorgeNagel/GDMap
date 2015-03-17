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
        csvwriter.writerow(['show_id', 'date'])
        for doc in docs:
            # Some recordings don't have a date in the search result
            date = doc.get('date', '')
            identifier = doc['identifier']
            csvwriter.writerow([identifier, date])


def show_identifiers():
    """Return a list of internetarchive show ids."""
    # Load whatever ids are currently stored in file
    if os.path.exists(SHOWS_FILENAME):
        ids = []
        with open(SHOWS_FILENAME, 'r') as fin:
            for line in fin:
                id_ = line.strip()
                ids.append(id_)
        return ids
    else:
        raise Exception("%s does not exist." % SHOWS_FILENAME)


if __name__ == '__main__':
    crawl_delay_seconds = int(sys.argv[1])
    download_shows(crawl_delay_seconds=crawl_delay_seconds)
