#!/bin/bash
sudo useradd --system --no-create-home --shell /sbin/nologin radicale
sudo chown -R radicale:radicale /etc/radicale /var/lib/radicale
sudo chmod -R 750 /etc/radicale /var/lib/radicale
sudo chmod 640 /etc/radicale/users
sudo mkdir -p /var/lib/radicale
sudo chown radicale:radicale /var/lib/radicale
# sudo -u radicale bash -c 'echo "localhost:5232:contacts_db:contacts_admin:db_pass" > /var/lib/radicale/.pgpass'
sudo chmod 600 /var/lib/radicale/.pgpass

#this creates a user to run the radicale server
