from fabric.api import run, hosts, task, env, local, cd

# Trick to get the ssh key
result = local('vagrant ssh-config | grep IdentityFile', capture=True)
env.key_filename = result.split()[1]

host = 'vagrant@127.0.0.1:2000'


@task
@hosts([host])
def reset_virtualenv():
    """Reset the python virtualenv."""
    with cd('gdmap'):
        run('sh reset_virtualenv.sh')


@task
@hosts([host])
def download_shows():
    with cd('gdmap'):
        run('virtualenv/bin/python download_shows.py')


@task
@hosts([host])
def test():
    """Run the unit tests."""
    with cd('gdmap'):
        run('virtualenv/bin/nosetests -s')
