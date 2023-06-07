import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
print('DEBUG.prod= ', DEBUG)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dm*#_9rs0r0z$g)65#m12y6wxl@rpw$%1dxu@+(x^dm*#_9rs0r0z$g)65#m12y6wv!=2b%"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["SQL_DATABASE"],
        "USER": os.environ["SQL_USER"],
        "PASSWORD": os.environ["SQL_PASSWORD"],
        "HOST": os.environ["SQL_HOST"],  # set in docker-compose.yml
        "PORT": os.environ["SQL_PORT"],  # default postgres port
    }
}
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CSRF_TRUSTED_ORIGINS = [
    'https://b2b.argentum.ua',
    'https://b2b.film.ua',
]
ADMINS = [('test admin1', 'andreyv@ukr.net'), ('test admin2', 'avoznyuk@film.ua')]
# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = [
    "b2b.film.ua",
    "127.0.0.1",
    "10.1.100.222",
]

EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = os.environ["EMAIL_PORT"]
EMAIL_USE_SSL = os.environ["EMAIL_USE_SSL"]
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_SUBJECT_PREFIX = os.environ["EMAIL_SUBJECT_PREFIX"]


try:
    from .local import *
except ImportError:
    pass
