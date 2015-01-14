import json
import logging
import time

from requests import get

logging.basicConfig(level=logging.INFO)

base_url = "https://archive.org/advancedsearch.php"
collection = "GratefulDead"
per_page = 100
crawl_delay_seconds = 1
start_page = 0


def internetarchive_search(collection='GratefulDead',
                           per_page=50,
                           start_page=0,
                           crawl_delay_seconds=1,
                           max_errors=10,
                           stop_page=None):
    page = start_page
    docs = []
    errors = 0
    while True:
        # Build the request
        query = "collection:(%s)&rows=%d&start=%d" % (
            collection, per_page, page)
        url = "%s?q=%s&output=json" % (base_url, query)
        logging.info("Requesting: %s" % url)

        # Get the search api response
        response = get(url)
        response_dict = response.json()
        status = response.status_code
        logging.debug("Response (%d): %s" % (status, response_dict))

        if status == 200:
            # Add the returned documents to the ongoing list
            requested_docs = response_dict['response']['docs']
            if not requested_docs:
                # We've passed the last page
                break
            docs.extend(requested_docs)
        else:
            errors += 1
            if errors > max_errors:
                raise Exception("Max Requests errors exceeded: %d" % errors)

        page += 1
        time.sleep(crawl_delay_seconds)
        if stop_page and page >= stop_page:
            break
    return docs

docs = internetarchive_search(collection='GratefulDead', per_page=100)
with open('shows.json', 'w') as fout:
    # Write a pretty print of the json results to file
    docs_json = json.dumps(docs, indent=4, sort_keys=True)
    fout.write(docs_json)
