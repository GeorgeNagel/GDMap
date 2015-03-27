# http://matthewminer.com/2015/01/25/docker-dev-environment-for-web-app.html
import os

# Use environment variable DEBUG=1 for server reloading on file updates
if int(os.environ.get('DEBUG', 0)):
    reload = True

bind = '0.0.0.0:80'
