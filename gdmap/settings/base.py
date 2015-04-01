import logging

MONGO_DATABASE_NAME = 'gdmap'
MONGO_CACHE_NAME = 'cache'

# The IP address is updated in /etc/hosts when the
# docker container named 'mongodb' is updated
MONGODB_HOST_NAME = 'mongodb'

MONGODB_PORT = 27017

CACHE_EXPIRATION_SECONDS = None

DATA_DIRECTORY = '/gdmap/data'

ELASTICSEARCH_INDEX_NAME = 'gdmap'

# This IP address is updated in /etc/hosts when the
# docker container named 'elasticsearch' is updated
ELASTICSEARCH_HOST_NAME = 'elasticsearch'

# Show flask debugging output
FLASK_DEBUG = False

logging.basicConfig(level=logging.WARNING)
