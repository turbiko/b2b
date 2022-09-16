FROM python:3.10.4-alpine3.14

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install "gunicorn==20.0.4"
# Install system packages required by Wagtail and Django.
# Install server packages
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev \
    && apk add jpeg-dev libwebp-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev libxml2-dev libxslt-dev libxml2

# Install python packages
RUN pip install --upgrade pip
RUN pip install "gunicorn==20.0.4"
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Postgres Entrypoint
COPY entrypoint.sh /usr/src/app/entrypoint.sh