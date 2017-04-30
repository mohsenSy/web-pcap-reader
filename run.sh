#!/bin/bash

cd /vagrant

python manage.py migrate

if ! nc -zv localhost 8000 2>/dev/null;
then
  (
  nohup python manage.py runserver 0:8000 > "$PWD/nohup.out" 2>&1
  if [ $? -ne 0 ]; then
    cat "$PWD/nohup.out"
    exit $?
  fi
  ) &
fi
