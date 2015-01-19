import logging
import requests

import requests_cache

from settings import CACHE_EXPIRATION_SECONDS

requests_cache.install_cache('cache',
                             backend='mongo',
                             expire_after=CACHE_EXPIRATION_SECONDS)
cache = requests_cache.core.get_cache()


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
