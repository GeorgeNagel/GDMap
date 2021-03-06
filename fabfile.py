from fabric.api import run, hosts, task, env, local, cd
from fabric.context_managers import shell_env

# Trick to get the ssh key
result = local('vagrant ssh-config | grep IdentityFile', capture=True)
env.key_filename = result.split()[1]
env.gdmap_path = '/home/vagrant/gdmap'

host = 'vagrant@127.0.0.1:2000'


@task
@hosts([host])
def clean():
    """Remove .pyc files."""
    run("find gdmap -name '*.pyc' -delete")


@task
@hosts([host])
def setup():
    """Set up the containers."""
    start_es()
    start_mongo()
    build_app()


@task
@hosts([host])
def start_es():
    """Star the elasticsearch container."""
    with cd('gdmap'):
        run("sudo docker run -d --name elasticsearch -p 9200:9200 elasticsearch:1.4.2")


@task
@hosts([host])
def start_mongo():
    """Star the mongodb container."""
    with cd('gdmap'):
        run("sudo docker run -d -p 27017:27017 --name mongodb dockerfile/mongodb")


@task
@hosts([host])
def start_nginx():
    """Start the nginx reverse-proxy container."""
    with cd('gdmap'):
        run("source scripts/start_nginx.sh")


@task
@hosts([host])
def start_docker_gen():
    """Start the service to generate nginx configuration files."""
    with cd('gdmap'):
        run("source scripts/start_docker_gen.sh")


@task
@hosts([host])
def build_app():
    """Build the webapp container."""
    with cd('gdmap'):
        run("sudo docker build -t webapp -f docker/webapp/Dockerfile .")


@task
@hosts([host])
def server():
    """Start the webapp server."""
    start_nginx()
    start_docker_gen()
    with cd('gdmap'):
        run(
            "sudo docker run --name app-instance -d -P"
            " --link elasticsearch:elasticsearch --link mongodb:mongodb"
            " -e VIRTUAL_HOST=localhost"
            " --volume=$(pwd):/gdmap webapp"
        )


@task
@hosts([host])
def dev_server():
    """Start the flask development webapp server."""
    with cd('gdmap'):
        run(
            "sudo docker run --name app-instance -d -p 0.0.0.0:80:80"
            " --link elasticsearch:elasticsearch --link mongodb:mongodb"
            " --volume=$(pwd):/gdmap webapp"
            " python dev_server.py"
        )


@task
@hosts([host])
def docker_cleanup():
    """Remove all running docker containers."""
    remove_container('nginx')
    remove_container('docker-gen')
    remove_container('app-instance')
    remove_container('mongodb')
    remove_container('elasticsearch')


@task
@hosts([host])
def remove_container(container):
    """Remove the specified container."""
    run("sudo docker rm -f {0} || echo No running {0} container".format(container))


@task
@hosts([host])
def docker_ps():
    """List all containers."""
    run("sudo docker ps -a")


@task
@hosts([host])
def download_shows():
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec -t -i app-instance python -m gdmap.data_scraping.archive_api.download_shows')


@task
@hosts([host])
def download_songs():
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec -t -i app-instance python -m gdmap.data_scraping.archive_api.download_songs')


@task
@hosts([host])
def index_songs():
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec -t -i app-instance python -m gdmap.es_index')


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
def download_show_listings():
    """Generate the list of locations."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec -t -i app-instance python -m gdmap.data_scraping.dead_net.download_show_listings')


@task
@hosts([host])
def geocode_locations():
    """Geocode the list of locations."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec -t -i app-instance python -m gdmap.data_scraping.geocode')


@task
@hosts([host])
def geocode_listings():
    """Geocode the listings from dead.net."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('sudo docker exec -t -i app-instance python -m gdmap.data_scraping.geocode_show_listings')


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
