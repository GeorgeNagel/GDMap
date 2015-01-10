# Remove the virtualenv, if it exists
rm -r virtualenv
# Create the virtualenv
virtualenv virtualenv
# Install the python requirements
virtualenv/bin/pip install -r requirements.txt

