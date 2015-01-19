import logging

from functools import wraps
from mongoengine import connect

from gdmap.settings import MONGO_DATABASE_NAME, MONGO_CACHE_NAME

db = connect(MONGO_DATABASE_NAME)
cache_db = connect(MONGO_CACHE_NAME)


def mongo_clean(f):
    """Drop the test databases."""
    @wraps(f)
    def wrapper(*args, **kwds):
        logging.debug('Dropping test databases')
        db.drop_database(MONGO_DATABASE_NAME)
        db.drop_database(MONGO_CACHE_NAME)
        return f(*args, **kwds)
    return wrapper
