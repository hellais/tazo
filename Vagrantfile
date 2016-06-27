# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 6379, host: 6379

  config.vm.provision "shell", inline: <<-EOF
  apt-get update
  apt-get install -y redis-server python-setuptools python-dev python-pip build-essential
  EOF
end
