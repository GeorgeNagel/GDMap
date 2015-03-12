"""Crawl the show listings on dead.net for location information."""
from bs4 import BeautifulSoup
import logging


from gdmap.data_scraping.utils import cache_request


def parse_show_page(response):
    """Parse an individual show page."""
    # Parse the html
    soup = BeautifulSoup(response.text)

    # Find the data on the page

    venue_el = soup.find('h3').a
    venue = venue_el.string

    h4_els = soup.findAll('h4')

    date_el = h4_els[0]
    date = date_el.string

    location_el = h4_els[1]
    location = location_el.string

    next_page_el = soup.select('div.nextshow a')[0]
    next_page_url = next_page_el.get('href')

    return {"date": date, "location": location, "venue": venue, "next": next_page_url}


def crawl_show_listings():
    """Crawl the show listings pages. Return structured show info."""
    # Crawl concerts in order, starting with the first show
    base_url = "http://www.dead.net"
    next_url = "http://www.dead.net/show/may-05-1965"
    results = []
    while next_url:
        response, cached = cache_request(next_url)
        status = response.status_code
        logging.info("Response %d Cached? %s" % (status, cached))
        if status == 200:
            parsed_result = parse_show_page(response)
            next_url = base_url + parsed_result.pop('next')
            results.append(parsed_result)
    return results


def unique_show_locations(listings):
    """
    Takes a list of data dicts scraped from dead.net.
    Returns a list of unique geocodable locations.
    """
    listing_geocodable = ['%s, %s' % (listing['venue'], listing['location']) for listing in listings]
    unique_geocodable = sorted(set(listing_geocodable))
    return unique_geocodable

if __name__ == "__main__":
    listings = crawl_show_listings()
    unique_locations = unique_show_locations(listings)
    with open('locations.txt', 'w') as fout:
        for location in unique_locations:
            fout.write("%s\n" % location)
