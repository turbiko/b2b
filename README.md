# b2b
pip install --upgrade pip

pip install wagtail

wagtail start  core .

python manage.py createsuperuser

pip install "gunicorn==20.0.4"

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic  --settings=core.settings.dev --no-input --clear

python manage.py update_index  --settings=core.settings.dev

https://github.com/phookycom/wagtailondocker 

https://www.phooky.com/blog/dockerize-wagtail-postgresql-as-a-development-environment/

docker-compose up -d --build

docker-compose exec web python manage.py createsuperuser --settings=core.settings.dev

docker-compose exec web python manage.py createsuperuser --settings=core.settings.production

