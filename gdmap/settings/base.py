import logging

MONGO_DATABASE_NAME = 'gdmap'
MONGO_CACHE_NAME = 'cache'

# 1 month cache expiration
CACHE_EXPIRATION_SECONDS = 60 * 60 * 24 * 30

# Show flask debugging output
FLASK_DEBUG = False

ELASTICSEARCH_INDEX_NAME = 'gdmap'

logging.basicConfig(level=logging.INFO)
