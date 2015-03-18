import logging

MONGO_DATABASE_NAME = 'gdmap'
MONGO_CACHE_NAME = 'cache'

CACHE_EXPIRATION_SECONDS = None

DATA_DIRECTORY = '/home/vagrant/gdmap/data'

# Show flask debugging output
FLASK_DEBUG = False

ELASTICSEARCH_INDEX_NAME = 'gdmap'

logging.basicConfig(level=logging.WARNING)
