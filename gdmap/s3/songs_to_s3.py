"""Upload songs .jl files to Amazon S3."""
import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from gdmap.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, SONGS_DIRECTORY

connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

bucket = connection.get_bucket(S3_BUCKET_NAME)

if __name__ == "__main__":
    for filename in os.listdir(SONGS_DIRECTORY):
        filepath = os.path.join(SONGS_DIRECTORY, filename)
        print "Copying %s" % filename
        key = Key(bucket)
        key.key = filename
        key.set_contents_from_filename(filepath)
