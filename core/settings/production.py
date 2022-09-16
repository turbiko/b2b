import os

from .base import *

DEBUG = False
print('Production DEBUG= ', DEBUG)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dpw$%1dxu@+(x^dm*#_9m12y6wxl@rpw$%1dxu@+(x^dm*#_9rs0r0z$pw$%1dxu@+(x^dm*#_96wv!=2b%"
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE"),
        'NAME': os.environ.get("SQL_DATABASE"),
        'USER': os.environ.get("SQL_USER"),
        'PASSWORD': os.environ.get("SQL_PASSWORD"),
        'HOST': os.environ.get("SQL_HOST"),
        'PORT': os.environ.get("SQL_PORT"),
    }
}

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["b2b.argentum.ua", "b2b.film.ua", "10.1.100.222"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
CSRF_TRUSTED_ORIGINS = ['https://*.argentum.ua','https://127.0.0.1','https://10.1.100.222']

try:
    from .local import *
except ImportError:
    pass
