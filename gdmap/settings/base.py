import logging

MONGO_DATABASE_NAME = 'gdmap'
MONGO_CACHE_NAME = 'cache'

CACHE_EXPIRATION_SECONDS = None

DATA_DIRECTORY = '/gdmap/data'

# Show flask debugging output
FLASK_DEBUG = False

ELASTICSEARCH_INDEX_NAME = 'gdmap'

# This IP address is updated in /etc/hosts when the
# docker container named 'elasticsearch' is updated
ELASTICSEARCH_HOST_NAME = 'elasticsearch'

logging.basicConfig(level=logging.WARNING)
