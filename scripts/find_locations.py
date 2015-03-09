"""Generate a list of locations from the index."""

from gdmap.es_index import query_es

locations_query_body = {
    'query': {
        # Return the locations for all documents
        'match_all': {}
    },
    'aggregations': {
        'locations_aggregation': {
            'terms': {
                'field': 'location',
                # Return all location buckets
                'size': 0
            }
        }
    },
    # Don't return query results, just the aggregation
    'size': 0
}


def find_locations():
    query_result = query_es(locations_query_body)
    location_buckets = query_result['aggregations']['locations_aggregation']['buckets']
    locations = [bucket['key'] for bucket in location_buckets]
    return locations


if __name__ == "__main__":
    locations = find_locations()
    with open('locations.txt', 'w') as fout:
        for location in locations:
            # Must encode unicode before writing to file
            location = location.encode('utf-8')
            fout.write("%s\n" % location)
