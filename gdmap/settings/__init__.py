from os import getenv

from base import *  # noqa

# Overwite base settings with any local settings
from local import *  # noqa

# Overwrite with test settings last for consistent test runs.
# Use test settings if the environment variable is set.
testing = bool(getenv("TESTING", 0))
if testing:
    print "USING TEST SETTINGS"
    from test import *  # noqa
