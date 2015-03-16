"""Geocode locations names."""
from csv import writer
import time

from geopy import GoogleV3

geolocator = GoogleV3()


def geocode_location(location_name):
    print "Geocoding %s." % location_name
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def geocode_locations():
    geocoded = {}
    with open('data/locations.txt', 'r') as fin:
        for location_name in fin:
            # When reading from a file, the lines will still have a \n character at the end
            # so we clean them out
            clean_location_name = location_name.strip()
            lat, lon = geocode_location(clean_location_name)
            geocoded[clean_location_name] = (lat, lon)
            # The Google Maps API rate limits requests
            time.sleep(1)
    with open('data/locations_geocoded.txt', 'w') as fout:
        csvwriter = writer(fout)
        location_names = sorted(geocoded.keys())
        for location_name in location_names:
            lat, lon = geocoded[location_name]
            csvwriter.writerow([location_name, lat, lon])


if __name__ == "__main__":
    geocode_locations()
