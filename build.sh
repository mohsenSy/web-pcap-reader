#!/bin/bash

cd /vagrant

apt-get install python-pip -y

pip install -r requirements.txt

python manage.py migrate

(
nohup python manage.py runserver 0:8000 > "$PWD/nohup.out" 2>&1
if [ $? -ne 0 ]; then
  cat "$PWD/nohup.out"
  exit $?
fi
) &
