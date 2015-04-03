# Grateful Dead Show Map and Search

## Setup the host machine

```bash
# Create the python virtual environment
$ virtualenv hostenv
# Install the python requirements
$ hostenv/bin/pip install -r requirements_host.txt
```

## Setup the vagrant box

```bash
$ vagrant up
```

## Create a local settings file

Local settings are not checked into git, as they may contain private keys.
Create your own settings file in gdmap/settings/local.py
```python
# Contents of gdmap/settings/local.py

# Put Flask in Debug mode for better error logging
FLASK_DEBUG = True
```

## Create the docker containers
```bash
$ hostenv/bin/fab setup
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
```

## Start the elasticsearch image

```bash
$ hostenv/bin/fab start_es
```

## Start the server

```bash
$ hostenv/bin/fab server

# When deploying to production, mount the volume wherever the git repo was cloned, e.g.
$ sudo docker run --name app-instance -d -p 0.0.0.0:80:80 --link elasticsearch:elasticsearch --link mongodb:mongodb --volume=/usr/local/src/gdmap:/gdmap webapp
```

## Run the tests

```bash
$ hostenv/bin/fab test
```

## Push up data to s3

```bash
$ hostenv/bin/fab upload_to_s3
```

## Download data from s3

```bash
$ hostenv/bin/fab download_from_s3
```

## Index the songs

```bash
$ hostenv/bin/fab index_songs
```

## Restart your VM

```bash
$ vagrant halt
$ vagrant up
```

## Close all running docker containers

```bash
$ hostenv/bin/fab docker_cleanup
```
