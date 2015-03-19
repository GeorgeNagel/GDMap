# Grateful Dead Show Map and Search

## Setup the host machine

```bash
# Create the python virtual environment
$ virtualenv hostenv
# Install the python requirements
$ hostenv/bin/pip install -r requirements_host.txt
```
## Install the [git submodules](http://www.git-scm.com/book/en/v2/Git-Tools-Submodules)

```bash
$ git submodule init
$ git submodule update
```

## Setup the vagrant box

```bash
$ vagrant up
```

## Create the python virtual environment in the VM and install dependencies

```bash
$ hostenv/bin/fab reset_virtualenv
```

## Create a local settings file

Local settings are not checked into git, as they may contain private keys.
Create your own settings file in gdmap/settings/local.py
```python
# Contents of gdmap/settings/local.py

# Put Flask in Debug mode for better error logging
FLASK_DEBUG = True
```

## Get data
```bash
# Download date and venue information from dead.net
$ hostenv/bin/fab download_show_listings
# Match venue and city names to latitude and longitude
$ hostenv/bin/fab geocode_locations
# Match the listings to a latitude and longitude
$ hostenv/bin/fab geocode_listings
# Download dates and ids for archive.org recordings
$ hostenv/bin/fab download_shows
# Download all of the songs
$ hostenv/bin/fab download_songs
# Download songs from only some years
$ hostenv/bin/fab download_songs:1967,1968
$ hostenv/bin/fab index_songs
```

## Start the server

```bash
$ hostenv/bin/fab server
```

## Restart your VM

```bash
$ vagrant halt
$ vagrant up
```

## If MongoDB gets locked

```bash
$ vagrant ssh
$ sudo rm -f /var/lib/mongodb/mongod.lock
$ sudo service mongodb restart
```

## Download data for cache

```bash
$ hostenv/bin/fab download_shows
$ hostenv/bin/fab download_songs
$ hostenv/bin/fab index_songs
```
