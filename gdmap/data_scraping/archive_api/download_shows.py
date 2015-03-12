import logging
import os
import sys
import time

from gdmap.data_scraping.utils import cache, json_request, APIException

logging.basicConfig(level=logging.INFO)

base_url = "https://archive.org/advancedsearch.php"
collection = "GratefulDead"
per_page = 100
crawl_delay_seconds = 1
start = 0

OUTPUT_FILENAME = "shows.txt"


def download_shows(collection='GratefulDead',
                   per_page=100,
                   start=0,
                   crawl_delay_seconds=1,
                   max_errors=10,
                   stop=None):
    docs = []
    errors = 0
    while True:
        # Build the request
        query = "collection:(%s)&rows=%d&start=%d" % (
            collection, per_page, start)
        url = "%s?q=%s&output=json" % (base_url, query)

        try:
            cached = cache.has_url(url)
            # Get the search api response
            response_dict = json_request(url)
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
    return docs


def show_identifiers(from_file=False, **kwargs):
    """Return a list of internetarchive show ids."""
    if from_file:
        # Load whatever ids are currently stored in file
        if os.path.exists(OUTPUT_FILENAME):
            ids = []
            with open(OUTPUT_FILENAME, 'r') as fin:
                for line in fin:
                    id_ = line.strip()
                    ids.append(id_)
            return ids
        else:
            raise Exception("%s does not exist." % OUTPUT_FILENAME)
    else:
        # Make the live requests
        docs = download_shows(**kwargs)
        ids = [doc['identifier'] for doc in docs]
        return ids

if __name__ == '__main__':
    crawl_delay_seconds = int(sys.argv[1])
    ids = show_identifiers(crawl_delay_seconds=crawl_delay_seconds)
    with open(OUTPUT_FILENAME, 'w') as fout:
        for id_ in ids:
            fout.write("%s\n" % id_)
