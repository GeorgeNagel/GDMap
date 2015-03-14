"""Generate a geocoded list of shows."""
from csv import reader, DictWriter

from gdmap.data_scraping.dead_net.crawl_show_listings import crawl_show_listings


def read_geocoded_locations():
    geocoded_locations = {}
    with open('data/locations_geocoded.txt', 'r') as fin:
        csvreader = reader(fin)
        for row in csvreader:
            location_name, lat, lon = row
            geocoded_locations[location_name] = (lat, lon)
    return geocoded_locations


def geocode_listings():
    """Geocode listings from dead.net"""
    geocoded_locations = read_geocoded_locations()
    listings = crawl_show_listings()
    # Match the listings against the geocoded location names
    geocoded_listings = []
    for listing in listings:
        location_name = '%s, %s' % (listing['venue'], listing['location'])
        location_name = location_name.encode('utf-8').strip()
        lat, lon = geocoded_locations[location_name]
        listing['lat'] = lat
        listing['lon'] = lon
        clean_venue = listing['venue'].encode('utf-8').strip()
        clean_location = listing['location'].encode('utf-8').strip()
        listing['venue'] = clean_venue
        listing['location'] = clean_location
        geocoded_listings.append(listing)
    return geocoded_listings


if __name__ == "__main__":
    geocoded_listings = geocode_listings()
    with open('data/geocoded_listings.txt', 'w') as fout:
        fieldnames = ['date', 'venue', 'location', 'lat', 'lon']
        writer = DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for listing in geocoded_listings:
            writer.writerow(listing)
