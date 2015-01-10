from fabric.api import run, hosts, task, env, local, cd

# Trick to get the ssh key
result = local('vagrant ssh-config | grep IdentityFile', capture=True)
env.key_filename = result.split()[1]

@task
@hosts(['vagrant@127.0.0.1:2000'])
def setup_vm():
    with cd('gdmap'):
        run('sh setup_vm.sh')

