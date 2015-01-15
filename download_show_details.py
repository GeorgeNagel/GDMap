import json
import logging
import time

import requests
import requests_cache

from download_shows import show_identifiers

logging.basicConfig(level=logging.INFO)

# 1 month cache expiration
cache_expiration_seconds = 2419200
requests_cache.install_cache('cache',
                             backend='sqlite',
                             expire_after=cache_expiration_seconds)
cache = requests_cache.core.get_cache()

base_url = 'https://archive.org/details'


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


def download_show_details(crawl_delay_seconds=1, max_errors=10, **kwargs):
    show_ids = show_identifiers(**kwargs)
    details = []
    errors = 0
    for id_ in show_ids:
        url = "%s/%s&output=json" % (base_url, id_)
        cached = cache.has_url(url)
        try:
            response_dict = internetarchive_json_api(url, **kwargs)
            details.append(response_dict)
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
    details = download_show_details()
    with open('details.json', 'w') as fout:
        # Write a pretty print of the json results to file
        docs_json = json.dumps(details, indent=4, sort_keys=True)
        fout.write(docs_json)
