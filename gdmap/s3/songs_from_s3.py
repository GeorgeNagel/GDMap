"""Download songs .jl files from Amazon S3."""
import os

from boto.s3.connection import S3Connection

from gdmap.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET_NAME, SONGS_DIRECTORY

connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

bucket = connection.get_bucket(S3_BUCKET_NAME)

if __name__ == "__main__":
    if not os.path.exists(SONGS_DIRECTORY):
        os.makedirs(SONGS_DIRECTORY)
    for key in bucket.list():
        output_filepath = os.path.join(SONGS_DIRECTORY, key.key)
        print "Copying %s" % output_filepath
        key.get_contents_to_filename(output_filepath)
