#!/usr/bin/env bash
# seting up web servers for the deployment of web_static

apt-get -y update > /dev/null
apt-get install -y nginx > /dev/null

# Creating the directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
touch /data/web_static/releases/test/index.html

echo "Hello this is Fake !!" > /data/web_static/releases/test/index.html

# if symbol lonk already exists remove it
if [ -d "/data/web_static/current" ]
then
	sudo rm -rf /data/web_static/current
fi

# creating the symbolic link to test
ln -sf /data/web_static/releases/test/ /data/web_static/current

# changing the ownership
chown -hR ubuntu:ubuntu /data

sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

service nginx restart
