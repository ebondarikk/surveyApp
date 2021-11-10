#! /bin/sh

set -e

echo "Waiting for postgres to get up and running..."
while ! nc -z survey-db 5432; do
  echo "waiting for postgres listening..."
  sleep 1
done
echo "PostgreSQL started"

ACTION=$1

if [ $ACTION ]; then
    sleep 2
    exec python manage.py $@
fi

exec gunicorn -w 2 -b 0.0.0.0:8000 --access-logfile - contec.wsgi:application
