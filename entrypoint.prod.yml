#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations --settings=biz.settings.production
python manage.py migrate --settings=biz.settings.production
python manage.py collectstatic --settings=biz.settings.production --no-input --clear
python manage.py update_index --settings=biz.settings.production
exec "$@"