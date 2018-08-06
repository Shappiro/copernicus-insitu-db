"""
Django settings for copernicus project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from getenv import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', False)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', env('ALLOWED_HOSTS')]
CSRF_TRUSTED_ORIGINS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_elasticsearch_dsl',
    'bootstrap3',
    'django_xworkflows',
    'hijack',
    'compat',
    'hijack_admin',
    'picklists',
    'insitu',
    'suit',
    'django.contrib.admin',
    'explorer',
]

if not DEBUG:
    import os

    INSTALLED_APPS += ['raven.contrib.django.raven_compat', ]

    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
    }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'insitu.context_processors.google_analytics',
                'insitu.context_processors.crazy_egg',
                'insitu.context_processors.sentry',

            ],
            'libraries':{
                'js': 'insitu.views.product',
            },
        },
    },
]

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
    },
}

MAX_RESULT_WINDOW = 10000  # This is ElasticSearch's default, but we define it
# here explicitly to minimize refactoring in case we ever change it.

# Django Suit customizations

SUIT_CONFIG = {
    'ADMIN_NAME': 'Copernicus Insitu DB'
}

LOGGING_CSV_FILENAME = env('LOGGING_CSV_FILENAME', 'user-actions-logging.csv')


GOOGLE_ANALYTICS_PROPERTY_ID = env('GOOGLE_ANALYTICS_PROPERTY_ID', '')

CRAZY_EGG = env('CRAZY_EGG', '')


# Hijack customization

HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/'
HIJACK_ALLOW_GET_REQUESTS = True

SUPPORT_EMAIL = env('SUPPORT_EMAIL', '')

EXPLORER_CONNECTIONS = {'Default': 'default'}
EXPLORER_SQL_WHITELIST = {'update_frequency', '_deleted', 'Update Frequency'}
EXPLORER_PERMISSION_VIEW = lambda u: u.is_authenticated
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_SCHEMA_EXCLUDE_TABLE_PREFIXES = [
    'auth_group', 'auth_group_permissions', 'auth_permission',
    'auth_user_groups', 'auth_user_user_permissions',
    'django_admin_log', 'django_content_type',
    'django_migrations', 'django_session',
    'explorer_query', 'explorer_querylog'
]
