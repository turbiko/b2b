

Admin panel for stuff users and superusers:

https://site.name.tld/admin # wagtail admin-panel

https://site.name.tld/django-admin  # Django admin-panel

Deploy to server fresh install:

git clone https://github.com/turbiko/b2b.git

cd ./b2b

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py collectstatic

docker --version

sudo docker images

docker container ls

sudo docker build -t b2b .

sudo docker run b2b

sudo docker exec -it <container_id> /bin/bash

Deploy ready to use from Git

*)db.sqlite3 exist and site with it work correctly

docker-compose up -d --build  # daemonize

docker-compose up  --build  # need run in tmux for disconnection issues

Create superuser for admin-panel:

docker-compose exec   <container_name> python manage.py createsuperuser --settings=core.settings.dev

or

docker-compose exec   <container_name> python manage.py createsuperuser --settings=core.settings.production



============
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
docker-compose up  --build
docker-compose down

docker-compose exec web python manage.py createsuperuser --settings=core.settings.dev

or

docker-compose exec web python manage.py createsuperuser --settings=core.settings.production


docker-compose exec web python manage.py sendchanges

# found after all code ready
some ideas and tuned functionality from Wagtail CRX coderedcms==2.1.2

