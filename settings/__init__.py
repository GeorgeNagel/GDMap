from os import getenv

from base import *  # noqa

# Use test settings if the environment variable is set
testing = bool(getenv("TESTING", 0))
if testing:
    print "USING TEST SETTINGS"
    from test import *  # noqa
