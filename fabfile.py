from fabric.api import run, hosts, task, env, local, cd
from fabric.context_managers import shell_env

# Trick to get the ssh key
result = local('vagrant ssh-config | grep IdentityFile', capture=True)
env.key_filename = result.split()[1]
env.gdmap_path = '/home/vagrant/gdmap'

host = 'vagrant@127.0.0.1:2000'


@task
@hosts([host])
def reset_virtualenv():
    """Reset the python virtualenv."""
    with cd('gdmap'):
        run('sh reset_virtualenv.sh')


@task
@hosts([host])
def clean():
    """Remove .pyc files."""
    run("find gdmap -name '*.pyc' -delete")


@task
@hosts([host])
def restart_mongo():
    """Restart the mongo service."""
    run('sudo rm -f /var/lib/mongodb/mongod.lock')
    run('sudo service mongodb restart')


@task
@hosts([host])
def download_shows(crawl_delay=1):
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/data_scraping/archive_api/download_shows.py %s' % crawl_delay)


@task
@hosts([host])
def download_songs(*years):
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/data_scraping/archive_api/download_songs.py %s' % ' '.join(years))


@task
@hosts([host])
def index_songs():
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/es_index.py')


@task
@hosts([host])
def test(*args):
    """Run the unit tests."""
    with cd('gdmap'):
        # If you don't supply a specific test to run, run on the project
        if not args:
            args = 'gdmap'
        run('sudo docker exec app-instance env TESTING=1 nosetests /gdmap/gdmap %s -s' % args)
        run('sudo docker exec app-instance env TESTING=1 flake8 gdmap')


@task
@hosts([host])
def server():
    """Run the server."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/run_server.py')


@task
@hosts([host])
def locations_from_mongo():
    """Generate a list of locations from songs in mongo."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python scripts/locations_from_mongo.py')


@task
@hosts([host])
def download_show_listings():
    """Generate the list of locations."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/data_scraping/dead_net/download_show_listings.py')


@task
@hosts([host])
def geocode_locations():
    """Geocode the list of locations."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/data_scraping/geocode.py')


@task
@hosts([host])
def geocode_listings():
    """Geocode the listings from dead.net."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/data_scraping/geocode_show_listings.py')


@task
@hosts([host])
def upload_to_s3():
    """Upload songs files to s3."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec app-instance python -m gdmap.s3.songs_to_s3')


@task
@hosts([host])
def download_from_s3():
    """Download songs files from s3."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec app-instance python -m gdmap.s3.songs_from_s3')
