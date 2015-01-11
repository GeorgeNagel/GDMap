# Grateful Dead Show Map and Search
## Setup the host machine
```
# Create the python virtual environment
$ virtualenv hostenv
# Install the python requirements
$ virtualenv/bin/pip install -r requirements_host.txt
```
## Setup the vagrant box
```
$ vagrant up
```
## Create the python virtual environment and install dependencies
```
$ virtualenv/bin/fab reset_virtualenv
```