# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = false

  config.vm.define "quantify.me" do |node|
    node.vm.box = "ubuntu1310-docker"
    node.vm.hostname = "quantify.me"
    node.vm.network :private_network, ip: '192.168.1.100'

    #node.vm.provision :shell, inline: "sed -i '/127.0.1.1/d' /etc/hosts"
    #node.vm.provision :hostmanager
  end

end
