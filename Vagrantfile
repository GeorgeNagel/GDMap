# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  # Ubuntu 14
  config.vm.box = "ubuntu/trusty64"

  # Allocate memory for the box
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end

  # Forward ssh
  config.vm.network :forwarded_port, id: "ssh", guest:22, host: 2000
  # Forward mongodb
  config.vm.network :forwarded_port, id: "mongo", guest: 27017, host: 27017, auto_correct: true
  # Forward site 80
  config.vm.network :forwarded_port, id: "site", guest: 80, host: 5000

  # Share the folder contents with the guest machine
  config.vm.synced_folder ".", "/home/vagrant/gdmap", owner: "vagrant", group: "vagrant"

  # Install docker
  config.vm.provision "shell", path: "provision.sh"
end
