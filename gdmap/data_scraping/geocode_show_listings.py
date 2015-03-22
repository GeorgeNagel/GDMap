"""Generate a geocoded list of shows."""
from datetime import datetime
from csv import reader, DictWriter, DictReader

from gdmap.data_scraping.dead_net.download_show_listings import crawl_show_listings


def read_geocoded_locations():
    geocoded_locations = {}
    with open('data/locations_geocoded.txt', 'r') as fin:
        csvreader = reader(fin)
        for row in csvreader:
            location_name, lat, lon = row
            geocoded_locations[location_name] = (lat, lon)
    return geocoded_locations


def read_geocoded_listings():
    geocoded_listings = []
    with open('data/geocoded_listings.txt', 'r') as fin:
        reader = DictReader(fin)
        for row in reader:
            geocoded_listings.append(row)
    return geocoded_listings


def geocoding_dict():
    """Create a dict mapping dates to geolocations, like:
    {
        'date 1': {
            'venue 1': {'lat': 5, 'lon': 6},
            'venue 2': {'lat: 6', 'lon': 7}
        },
        'date 2': {
            ...
        },
        ...
    }
    """
    listings = read_geocoded_listings()
    geo_dict = {}
    for listing in listings:
        date_text = listing['date']
        date_iso = datetime.strptime(date_text, '%B %d, %Y').date().isoformat()
        venue = listing['venue']
        lat = listing['lat']
        lon = listing['lon']
        if date_iso not in geo_dict:
            geo_dict[date_iso] = {}
        if venue not in geo_dict[date_iso]:
            geo_dict[date_iso][venue] = {'lat': lat, 'lon': lon}
    return geo_dict


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
    print "Geocoding listings"
    geocoded_listings = geocode_listings()
    print "Writing geocoded listings to file"
    with open('data/geocoded_listings.txt', 'w') as fout:
        fieldnames = ['date', 'venue', 'location', 'lat', 'lon']
        writer = DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for listing in geocoded_listings:
            writer.writerow(listing)
