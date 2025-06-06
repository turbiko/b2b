# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from dotenv import load_dotenv

from django.core.management import utils
from django.utils.translation import gettext_lazy as _


load_dotenv()

DATE_FORMAT = 'd F Y'
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/



# Application definition

INSTALLED_APPS = [
    # This project
    "home",
    # Wagtail CRX (CodeRed Extensions)
    # "coderedcms",
    "django_bootstrap5",
    # "wagtailcache",
    # "wagtailseo",
    # Wagtail
    "search",
    'wagtail.api.v2',
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "wagtail_localize",
    "wagtail_localize.locales",
    "wagtail.contrib.modeladmin",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # added other ready to use functionality/modules
    "modelcluster",
    "taggit",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',

    # added code
    'menus.apps.MenusConfig',
    'project.apps.ProjectConfig',
    'contacts.apps.ContactsConfig',
    # 'company.apps.CompanyConfig',
]

MIDDLEWARE = [
    # Save pages to cache. Must be FIRST.
    # "wagtailcache.cache.UpdateCacheMiddleware",
    # Common functionality
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Security
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    #  Error reporting. Uncomment this to receive emails when a 404 is triggered.
    # 'django.middleware.common.BrokenLinkEmailsMiddleware',
    # CMS functionality
    "whitenoise.middleware.WhiteNoiseMiddleware",  # production caching
    "django.middleware.locale.LocaleMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # Fetch from cache. Must be LAST.
    # "wagtailcache.cache.FetchFromCacheMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATE_DIR = os.path.join(PROJECT_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATE_DIR,
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "uk"

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('uk', _('Ukrainian')),
    ('en', _('English')),
]

TIME_ZONE = "UTC"

USE_I18N = True

WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_TZ = True

# https://docs.wagtail.org/en/stable/reference/contrib/simple_translation.html
WAGTAILSIMPLETRANSLATION_SYNC_PAGE_TREE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Wagtail

WAGTAIL_SITE_NAME = "b2b.film.ua"
WAGTAILADMIN_BASE_URL = "http://b2b.film.ua"

WAGTAIL_ENABLE_UPDATE_CHECK = False

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://b2b.argentum.ua"

# Tags

TAGGIT_CASE_INSENSITIVE = True

# Sets default for primary key IDs
# See https://docs.djangoproject.com/en/4.1/ref/models/fields/#bigautofield
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Wagtail settings options
# https://docs.wagtail.org/en/stable/reference/settings.html
DEFAULT_FROM_EMAIL = 'noreply@argentum.ua'
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'noreply@argentum.ua'
WAGTAILUSERS_PASSWORD_REQUIRED = True
WAGTAILADMIN_NOTIFICATION_USE_HTML = True
WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS = False

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.argentum.ua'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'noreply@argentum.ua'
EMAIL_HOST_PASSWORD = '8gZ3---XXhL'
EMAIL_SUBJECT_PREFIX = 'b2b |'

# Login

# LOGIN_URL = "wagtailadmin_login"
# LOGIN_REDIRECT_URL = "wagtailadmin_home"

# https://learnwagtail.com/tutorials/adding-user-authentication-registration-and-login-your-wagtail-website/
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_REDIRECT_URL = '/login/'
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ["admin", "root"]
ACCOUNT_USERNAME_MIN_LENGTH = 4

WAGTAILIMAGES_MAX_UPLOAD_SIZE = 15 * 1024 * 1024 * 1024  # first digit size in GB
WAGTAILDOCS_SERVE_METHOD = 'redirect'  # need security check for pages  is_authentificated

# https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
PREVIEW_EXT = ['.jpg', '.jpeg', '.pjpeg', '.pjp', '.png', '.ico', '.cur', '.tif', '.tiff', '.bmp', '.gif', '.eps',
               '.svg', '.webp', '.apng', '.avif', '.jfif', '.mp4']

PICTURE_EXT = ['.jpg', '.jpeg', '.pjpeg', '.pjp', '.png', '.ico', '.cur', '.tif', '.tiff', '.bmp', '.gif', '.eps',
               '.svg', '.webp', '.apng', '.avif', '.jfif']
PICTURE_ICON = "/media/images/image.svg"

VIDEO_EXT = [ '.mp4' ]
VIDEO_ICON = "/media/images/file-play.svg"
DEFAULT_DOWNLOAD_ICON = "/media/images/download.svg"

DOCUMENT_EXT = ['']

LOGGING = {
    'version': 1,
    # The version number of our log
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {name} {levelname} {module} {message}',
            'style':  '{',
        },
        'simple':  {
            'format': '{asctime} {levelname} {message}',
            'style':  '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log

    #    DEBUG (10) detailed
    #    INFO (20) informational, all ok but let me know that
    #    WARNING (30) something wrong, but application will continue
    #    ERROR (40) application can`t do someting
    #    CRITICAL (50) application will crash

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/' + 'warning.log',
            'formatter': 'verbose'
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    'loggers': {
        'project': {
            'handlers':  ['file'],  # notice how file variable is called in handler which has been defined above
            'level':     'INFO',  # CRITICAL ERROR WARNING INFO DEBUG
            'propagate': True,
            'formatter': 'verbose'
        },
       # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        '': {
            'handlers': ['console', 'file'], #notice how file variable is called in handler which has been defined above
            'level': 'DEBUG',
            'propagate': True,
            'formatter': 'verbose'
        },
    },
}

FILE_UPLOAD_HANDLERS = ["django.core.files.uploadhandler.MemoryFileUploadHandler",
                        "django.core.files.uploadhandler.TemporaryFileUploadHandler"]
