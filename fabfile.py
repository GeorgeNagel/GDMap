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
def download_shows(crawl_delay=1):
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/archive_api/download_shows.py %s' % crawl_delay)


@task
@hosts([host])
def download_songs(crawl_delay=1):
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/archive_api/download_songs.py %s' % crawl_delay)


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
        with shell_env(TESTING='1'):
            run('virtualenv/bin/flake8 gdmap')
            # If you don't supply a specific test to run, run on the project
            if not args:
                args = 'gdmap'
            run('virtualenv/bin/nosetests %s -s' % args)


@task
@hosts([host])
def server():
    """Run the unit tests."""
    with cd('gdmap'):
        with shell_env(PYTHONPATH=env.gdmap_path):
            run('virtualenv/bin/python gdmap/run_server.py')
