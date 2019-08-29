"""
Django settings for copernicus project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from getenv import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', False)
DEBUG_TOOLBAR = env('DEBUG_TOOLBAR', False)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', env('ALLOWED_HOSTS')]
CSRF_TRUSTED_ORIGINS = env('ALLOWED_HOSTS')

# Sentry
SENTRY_DSN = env('SENTRY_DSN', '')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()]
    )

    SENTRY_ORG_SLUG = env('SENTRY_ORG_SLUG', '')
    SENTRY_PROJ_SLUG = env('SENTRY_PROJ_SLUG', '')
    SENTRY_AUTH_TOKEN = env('SENTRY_AUTH_TOKEN', '')
    SENTRY_BASE_URL = f"https://sentry.io/api/0/projects/{SENTRY_ORG_SLUG}/{SENTRY_PROJ_SLUG}/"

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_elasticsearch_dsl',
    'bootstrap3',
    'django_xworkflows',
    'hijack',
    'compat',
    'docs',
    'explorer',
    'hijack_admin',
    'suit',
    'wkhtmltopdf',
    'picklists',
    'insitu',
]

if not DEBUG:
    import os

    INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]

    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
    }

if DEBUG_TOOLBAR:
    INSTALLED_APPS += ['debug_toolbar',]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG_TOOLBAR:
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

ROOT_URLCONF = 'copernicus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'insitu.context_processors.base',
                'insitu.context_processors.matomo',
                'insitu.context_processors.crazy_egg',
                'insitu.context_processors.sentry',
                'insitu.context_processors.statistics',
            ],
            'libraries':{
                'js': 'insitu.views.product',
            },
        },
    },
]
WKHTMLTOPDF_CMD = '/usr/bin/wkhtmltopdf'
WSGI_APPLICATION = 'copernicus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'PORT': 5432,
        'NAME': env('POSTGRES_DB', 'insitu'),
        'USER': env('POSTGRES_USER', 'insitu'),
        'PASSWORD': env('POSTGRES_PASSWORD', 'insitu'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

READ_ONLY_GROUP = env('READ_ONLY_GROUP', 'ReadOnly')

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TZ', 'Europe/Copenhagen')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': env('ELASTICSEARCH_HOST'),
        'http_auth': env('ELASTICSEARCH_AUTH'),
        'timeout': env('ELASTICSEARCH_TIMEOUT', 120),
    },
}

MAX_RESULT_WINDOW = 10000  # This is ElasticSearch's default, but we define it
# here explicitly to minimize refactoring in case we ever change it.

# Django Suit customizations

SUIT_CONFIG = {
    'ADMIN_NAME': 'Copernicus Insitu DB'
}

LOGGING_CSV_FILENAME = env('LOGGING_CSV_FILENAME', 'user-actions-logging.csv')
LOGGING_CSV_PATH = os.path.join(BASE_DIR, 'logging', LOGGING_CSV_FILENAME)

MATOMO = env('MATOMO', False)

CRAZY_EGG = env('CRAZY_EGG', '')


# Hijack customization

HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/'
HIJACK_ALLOW_GET_REQUESTS = True

SUPPORT_EMAIL = env('SUPPORT_EMAIL', '')

EXPLORER_CONNECTIONS = {'Default': 'default'}
EXPLORER_DEFAULT_ROWS = 50000
EXPLORER_SQL_WHITELIST = {'update_frequency', '_deleted', 'Update Frequency', 'picklists_updatefrequency', 'Data updated', 'data_updated'}


def EXPLORER_PERMISSION_VIEW(u): return u.is_authenticated


EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES = [
    'auth_group', 'auth_group_permissions', 'auth_permission',
    'auth_user_groups', 'auth_user_user_permissions',
    'django_admin_log', 'django_content_type',
    'django_migrations', 'django_session',
    'explorer_query', 'explorer_querylog'
]

DOCS_ROOT = os.path.join(BASE_DIR, 'docs/_build/html')
DOCS_ACCESS = 'login_required'

EMAIL_BACKEND = env('EMAIL_BACKEND',
                    'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', 'localhost')
EMAIL_PORT = env('EMAIL_PORT', 25)
EMAIL_SENDER = env('EMAIL_SENDER', '')

SITE_URL = env('SITE_URL', '')

if DEBUG_TOOLBAR:
    def show_toolbar(request):
        return request.user.is_authenticated() and request.user.is_superuser

    INTERNAL_IPS=ALLOWED_HOSTS

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'copernicus.settings.show_toolbar',
        # Rest of config
    }
