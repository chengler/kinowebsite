"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
# in privat_settings ?
# from django.contrib.messages import constants as message_constants
# MESSAGE_LEVEL = 10  # DEBUG default 20= Info; 40 Error
from .privat_settings import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

### the importetd stuff

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '***'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
# ALLOWED_HOSTS = ['mobilephone', '127.0.0.1']
# DEFAULT_DOMAIN = 'http://127.0.0.1:8000'

# https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = ''
#EMAIL_PORT = 587
#EMAIL_SUBJECT_PREFIX = '[MySite]'
#EMAIL_USE_LOCALTIME = False
#EMAIL_USE_TLS = True
#EMAIL_HOST_PASSWORD = ''
#EMAIL_HOST_USER = '@'

###


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'crispy_forms',
    'django_bootstrap5',
    'crispy_bootstrap5',
    'filme.apps.FilmeConfig',
    'polls.apps.PollsConfig',
    'django_extensions', 
    'django.forms',
    'maintenance_mode',
]
CRISPY_TEMPLATE_PACK = 'bootstrap5' # neu
CRISPY_TEMPLATE_PACK = 'bootstrap5' # neu

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting' # ClearableFileInput

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


if DEBUG:
    STATICFILES_DIRS = [    os.path.join(BASE_DIR, "static"),]
    STATIC_ROOT = os.path.join(BASE_DIR, '')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')




MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SECURE_HSTS_SECONDS = '0' # acuh http ermöglichen
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#         'LOCATION': '/tmp/memcached.sock',
#     }
# }
# CACHE_MIDDLEWARE_ALIAS = "cache"
# CACHE_MIDDLEWARE_SECONDS = 600

# https://pypi.org/project/django-maintenance-mode/
MAINTENANCE_MODE = None # None True
# if True admin site will not be affected by the maintenance-mode page
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = False

