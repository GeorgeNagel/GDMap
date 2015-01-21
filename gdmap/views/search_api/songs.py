from flask.ext.restful import Resource, reqparse

from gdmap import api

parser = reqparse.RequestParser()

# Search by song title
parser.add_argument('song_title', type=str)

# Search by sha1
parser.add_argument('sha1', type=str)


class SongResource(Resource):
    # Define the access point for this resource
    uri = '/api/songs/'

    # Handle HTTP GET requests
    def get(self):
        args = parser.parse_args()
        return {'args': args}

# Add the endpoint to the search API
api.add_resource(SongResource, SongResource.uri)
