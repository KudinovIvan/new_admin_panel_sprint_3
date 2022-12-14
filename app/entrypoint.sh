#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      echo "Waiting for postgres"
      sleep 0.1
done

python manage.py migrate && python manage.py collectstatic --clear --noinput && uwsgi --ini /etc/uwsgi.ini