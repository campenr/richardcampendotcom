# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.synced_folder ".", "/home/vagrant/campenco", create: true

  config.vm.network "private_network", ip: "192.168.50.110"

  config.vm.network "forwarded_port", guest: 80, host: 5010

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "ansible/playbook.yml"
    ansible.inventory_path = "ansible/hosts.ini"
    ansible.limit = "development"
    ansible.verbose = true
  end

  config.vm.provider "virtualbox" do |v|
    v.linked_clone = true
  end

end
