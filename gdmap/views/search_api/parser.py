from flask.ext.restful import reqparse

# Create a parser to parse arguments for the songs endpoints
parser = reqparse.RequestParser()

# Query on all text fields
parser.add_argument('q', type=str)

# Search by song title
parser.add_argument('title', type=str)

# Search by sha1
parser.add_argument('sha1', type=str)

# Search by location name
parser.add_argument('location', type=str)

# Search by track number
parser.add_argument('track', type=int)

# Filter by album name (concert name)
parser.add_argument('album', type=str)

# Results per page
parser.add_argument('per_page', type=int)

# Page number
parser.add_argument('page', type=int)

# Date min
parser.add_argument('date_gte', type=str)

# Date max
parser.add_argument('date_lte', type=str)

# Sort order
parser.add_argument('sort', type=str)
parser.add_argument('sort_order', type=str)
