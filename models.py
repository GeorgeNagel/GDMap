from mongoengine import Document, fields, connect

from settings import MONGO_DATABASE_NAME

# Establish the connection to the database
connect(MONGO_DATABASE_NAME)


class Song(Document):
    """A mongoengine document representing a single song."""
    sha1 = fields.StringField(
        help_text="Unique identifier for this file.",
        primary_key=True)
    show_id = fields.StringField(
        help_text="The Archive.org ID representing the show recording.",
        required=True)
    filename = fields.StringField(
        help_text="The Arhchive.org filename for this recording.",
        required=True)
    album = fields.StringField(
        help_text="The concert name.",
        required=True)
    title = fields.StringField(
        help_text="The name of the song",
        required=True)
    track = fields.IntField(
        help_text="The order of the track in the set. 1-indexed.",
        required=True)
