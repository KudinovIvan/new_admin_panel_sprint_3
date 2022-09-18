#!/usr/bin/env bash

set -e

chown www-data:www-data /var/log

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      echo "Waiting for postgres"
      sleep 0.1
done

while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      echo "Waiting for es"
      sleep 0.1
done

python main.py