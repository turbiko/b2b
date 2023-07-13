import os
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
print('DEBUG.dev= ', DEBUG)

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

WAGTAIL_CACHE = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME":   os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = [
    "b2b.argentum.ua",
    "b2b.film.ua",
    "10.1.100.222",
    '127.0.0.1',
    'localhost',
]

ADMINS = [('test admin1', 'a.voznyuk@film.ua'), ('test admin2', 'avoznyuk@film.ua')]
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CSRF_TRUSTED_ORIGINS = ['https://*.argentum.ua',
                        'https://*.film.ua',
                        'https://127.0.0.1',
                        'https://10.1.100.222'
                        ]

DEBUG404 = False

try:
    from .local import *
except ImportError:
    pass
