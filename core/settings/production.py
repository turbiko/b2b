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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME":   os.path.join(BASE_DIR, "db.sqlite3"),
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
    "b2b.argentum.ua",
    "b2b.film.ua",
    "127.0.0.1",
    "10.1.100.222",
]

try:
    from .local import *
except ImportError:
    pass
