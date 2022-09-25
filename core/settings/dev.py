import os

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
print('DEBUG= ', DEBUG)

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
# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': os.environ.get("SQL_ENGINE"),
#             'NAME': os.environ.get("SQL_DATABASE"),
#             'USER': os.environ.get("SQL_USER"),
#             'PASSWORD': os.environ.get("SQL_PASSWORD"),
#             'HOST': os.environ.get("SQL_HOST"),
#             'PORT': os.environ.get("SQL_PORT"),
#         }
#     }
# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["b2b.argentum.ua", "b2b.film.ua", "10.1.100.222", '127.0.0.1']

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CSRF_TRUSTED_ORIGINS = ['https://*.argentum.ua','https://*.film.ua','https://127.0.0.1','https://10.1.100.222']

DEBUG404 = False

try:
    from .local import *
except ImportError:
    pass
