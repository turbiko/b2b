#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    echo "HOST: "$SQL_HOST $SQL_PORT

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi


python manage.py makemigrations --settings=core.settings.dev
python manage.py migrate --settings=core.settings.dev
python manage.py collectstatic --settings=core.settings.production --no-input --clear
#python manage.py update_index --settings=core.settings.dev
gunicorn core.wsgi:application -b :8000
exec "$@"