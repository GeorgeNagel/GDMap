"""Generate a list of locations from the index."""

from mongoengine import connect

from gdmap.models import Song
from gdmap.settings import MONGO_DATABASE_NAME


# Establish the connection to the database
connect(MONGO_DATABASE_NAME)


def find_locations():
    locations = [loc for loc in Song.objects.all().distinct('location')]
    return locations


if __name__ == "__main__":
    locations = find_locations()
    with open('data/locations_from_mongo.txt', 'w') as fout:
        for location in locations:
            # Must encode unicode before writing to file
            location = location.encode('utf-8')
            fout.write("%s\n" % location)
