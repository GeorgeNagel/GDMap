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

## Start the development server

Use this when altering static/template files.

```bash
$ hostenv/bin/fab dev_server
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

# Deploy steps

1. Create new droplet, change password.
    
    Point dns records in namecheap to ip address of droplet.

    ```
            Hostname=@   IP/URL=http://www.goldenroadmap.com/   Record=URL Redirect TTL=1800
            Hostname=www IP/URL=45.55.185.140   Record=A (Address)     TTL=60
    ```

2. Install git.
    
    ```bash
    $ apt-get update
    $ apt-get install git
    ```

3. Install docker
    
    ```bash
    $ /bin/bash provision.sh
    ```

4. Setup containers

    ```bash
    $ sudo docker run -d --name elasticsearch -p 9200:9200 elasticsearch:1.4.2
    $ sudo docker run -d -p 27017:27017 --name mongodb dockerfile/mongodb
    $ source scripts/start_nginx.sh
    $ source scripts/start_docker_gen.sh
    ```

5. Build the webapp

    ```bash
    $ sudo docker build -t webapp -f docker/webapp/Dockerfile .
    ```

6. Create local settings file with AWS credentials
7. Start the webapp

    ```bash
    $ sudo docker run --name app1 -d -P --link elasticsearch:elasticsearch --link mongodb:mongodb -e VIRTUAL_HOST=www.goldenroadmap.com --volume=$(pwd):/gdmap webapp
    ```

8. Pull data from S3

    ```bash
    $ sudo docker exec app1 -m gdmap.s3.songs_from_s3
    ```

9. Index the songs

    ```bash
    $ sudo docker exec -t -i app1 python -m gdmap.es_index
    ```
