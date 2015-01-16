import json
import logging
import time

import requests
import requests_cache

logging.basicConfig(level=logging.INFO)

# 1 week cache expiration
cache_expiration_seconds = 604800
requests_cache.install_cache('cache',
                             backend='mongo',
                             expire_after=cache_expiration_seconds)
cache = requests_cache.core.get_cache()

base_url = "https://archive.org/advancedsearch.php"
collection = "GratefulDead"
per_page = 100
crawl_delay_seconds = 1
start = 0


def internetarchive_search(collection='GratefulDead',
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

        # Get the search api response
        logging.info("Requesting: %s" % url)
        cached = cache.has_url(url)
        response = requests.get(url)
        response_dict = response.json()
        status = response.status_code
        logging.info("Response %d Cached? %s" % (status, cached))

        if status == 200:
            # Add the returned documents to the ongoing list
            requested_docs = response_dict['response']['docs']
            if not requested_docs:
                # We've passed the last page
                break
            docs.extend(requested_docs)
        else:
            logging.error("Error (%d) downloading: %s" % (status, url))
            errors += 1
            if errors > max_errors:
                raise Exception("Max Requests errors exceeded: %d" % errors)

        start = start + per_page
        if not cached:
            # We did not just hit our cache, so be a good neighbor and sleep
            time.sleep(crawl_delay_seconds)
        if stop and start >= stop:
            break
    return docs


def show_identifiers(**kwargs):
    docs = internetarchive_search(**kwargs)
    ids = [doc['identifier'] for doc in docs]
    return ids

if __name__ == '__main__':
    docs = internetarchive_search()
    with open('shows.json', 'w') as fout:
        # Write a pretty print of the json results to file
        docs_json = json.dumps(docs, indent=4, sort_keys=True)
        fout.write(docs_json)
