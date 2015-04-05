############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Maintaner Name

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl

# Install Python and Basic Python Tools
RUN apt-get install -y python python-pip

# Add the requirements file
ADD /requirements.txt /gdmap/requirements.txt

# Use pip to download and install requirements:
RUN pip install -r /gdmap/requirements.txt

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /gdmap

# Add the app folder to the python path
ENV PYTHONPATH="/gdmap/gdmap"

# Set the default command to execute    
# when creating a new container
# i.e. using gunicorn to serve the application
CMD ["gunicorn", "--config=gunicorn.py", "gdmap:app"]