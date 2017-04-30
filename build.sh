#!/bin/bash

cd /vagrant

apt-get install python-pip -y

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver 0:8000 &
