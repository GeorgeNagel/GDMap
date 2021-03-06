import logging
import requests

from pymongo import Connection
import requests_cache

from gdmap.settings import CACHE_EXPIRATION_SECONDS, MONGO_CACHE_NAME, MONGODB_HOST_NAME, MONGODB_PORT

connection = Connection(MONGODB_HOST_NAME, MONGODB_PORT)
requests_cache.install_cache(cache_name=MONGO_CACHE_NAME,
                             backend='mongo',
                             expire_after=CACHE_EXPIRATION_SECONDS,
                             connection=connection)
cache = requests_cache.core.get_cache()


class APIException(Exception):
    pass


def cache_request(url):
    logging.info("Requesting: %s" % url)
    cached = cache.has_url(url)
    response = requests.get(url)
    return response, cached


def json_request(url):
    """Make a cachable request to a JSON endpoint."""
    # Get the json response
    response, cached = cache_request(url)
    response_dict = response.json()

    status = response.status_code
    logging.info("Response %d Cached? %s" % (status, cached))
    if status == 200:
        return response_dict, cached
    else:
        raise APIException("Error (%d) downloading: %s" % (status, url))
