import os
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
print('DEBUG.prod= ', DEBUG)
#
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATIC_URL = "/static/"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dm*#_9rs0r0z$g)65#m12y6wxl@rpw$%1dxu@+(x^dm*#_9rs0r0z$g)65#m12y6wv!=2b%"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME":   os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "b2b.film.ua <noreply@argentum.ua>"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CSRF_TRUSTED_ORIGINS = [
    'https://b2b.argentum.ua',
    'https://b2b.film.ua',
]

# A list of people who get error notifications.
ADMINS = [('admin', 'andreyv@ukr.net'), ('admin2', 'avoznyuk@film.ua')]

# A list in the same format as ADMINS that specifies who should get broken link
# (404) notifications when BrokenLinkEmailsMiddleware is enabled.
MANAGERS = ADMINS

# Email address used to send error messages to ADMINS.
SERVER_EMAIL = "Error " + DEFAULT_FROM_EMAIL

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

try:
    from .local import *
except ImportError:
    pass
