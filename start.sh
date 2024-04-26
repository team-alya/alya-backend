#!/bin/bash -x

python3 /alyabackend/manage.py migrate

exec python3 /alyabackend/manage.py runserver 0.0.0.0:8000
