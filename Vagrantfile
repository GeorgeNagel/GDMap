# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "hashicorp/precise32"

  # Forward ssh
  config.vm.network :forwarded_port, id: "ssh", guest:22, host: 2000
  # Forward mongodb
  config.vm.network :forwarded_port, id: "mongo", guest: 27017, host: 27017, auto_correct: true
  config.vm.network :forwarded_port, id: "site", guest: 5000, host: 5000

  # Share the folder contents with the guest machine
  config.vm.synced_folder ".", "/home/vagrant/gdmap", owner: "vagrant", group: "vagrant"

  # Provision with Puppet
  config.vm.provision "shell", path: "puppet/pre_provision.sh"
  config.vm.provision "puppet" do |puppet|
    puppet.manifests_path = "puppet"
    puppet.manifest_file  = "manifest.pp"
    puppet.module_path = "puppet/modules"
    puppet.options = "--verbose"
  end
end
