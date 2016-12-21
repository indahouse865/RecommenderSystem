#!/bin/bash

#run using sudo command
#make sure you have the setup redis.conf in the same folder as this script

#PREREQUISITES
apt-get update
apt-get install build-essential tcl

#DOWNLOAD REDIS
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable

#INSTALL
make
make test
make install

#CONFIG
mkdir /etc/redis
cp redis.conf /etc/redis

cat > /etc/systemd/system/redis.service <<- EOM
/etc/systemd/system/redis.service
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
User=redis
Group=redis
ExecStart=/usr/local/bin/redis-server /etc/redis/redis.conf
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always

[Install]
WantedBy=multi-user.target
EOM

#PERMISSIONS
adduser --system --group --no-create-home redis
mkdir /var/lib/redis
chown redis:redis /var/lib/redis
chmod 770 /var/lib/redis

#START AND CHECK SERVICE
systemctl start redis
systemctl status redis
systemctl enable redis

