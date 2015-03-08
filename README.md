# Grateful Dead Show Map and Search

## Setup the host machine

```bash
# Create the python virtual environment
$ virtualenv hostenv
# Install the python requirements
$ virtualenv/bin/pip install -r requirements_host.txt
```

## Setup the vagrant box

```bash
$ vagrant up
```

## Create the python virtual environment and install dependencies

```bash
$ virtualenv/bin/fab reset_virtualenv
```

## Start the server

```bash
$ source hostenv/bin/activate
$ vagrant up
$ fab server
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
$ fab download_shows
$ fab download_songs
$ fab index_songs
```
