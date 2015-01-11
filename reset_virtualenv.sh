# Remove the virtualenv, if it exists
rm -fr virtualenv
# Create the virtualenv
virtualenv virtualenv
# Install the python requirements
virtualenv/bin/pip install -r requirements.txt

