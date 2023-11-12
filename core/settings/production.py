import os
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
print('DEBUG.prod= ', DEBUG)

# SECRET_KEY = utils.get_random_secret_key()
SECRET_KEY = os.getenv("SECRET_KEY", "prod-secret-key-ryu_zr&i&2ne6kXt9uib5oy8rca6ygb5tv!5hb#po-%%9hn2_43k")
print('prod SECRET_KEY: ', SECRET_KEY)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME":   os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

"""
#  https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial
# psycopg2-binary
# python -m pip install psycopg2-binary==2.9.6
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
"""

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "b2b.film.ua <noreply@argentum.ua>"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CSRF_TRUSTED_ORIGINS = [
    'https://b2b.film.ua',
]

# A list of people who get error notifications.
ADMINS = [('Developer', 'a.voznyuk@film.ua')]

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = f"Error {DEFAULT_FROM_EMAIL}"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = [
    "b2b.argentum.ua",
    "b2b.film.ua",
    "10.1.100.222",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache"),  # noqa
        "KEY_PREFIX": "b2b_cache",
        "TIMEOUT": 120,  # in seconds 14400
    }
}


# try:
#     from .local import *
# except ImportError:
#     pass
