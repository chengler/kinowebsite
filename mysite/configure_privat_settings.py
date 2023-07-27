#  mysite/privat_settings.py
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = 10  # DEBUG default 20= Info; 40 Error
#DEBUG = False
DEBUG = True

ALLOWED_HOSTS = [ '127.0.0.1']
DEFAULT_DOMAIN = 'https://Meine.Domain'
SECRET_KEY = 'YOUR_KEY_HERE(_#4g7&iljthr&5!*90#oo%fp!-1(!r%i42&*e<F2>w&@-0@(&bykwgbba'
# https://docs.djangoproject.com/en/3.0/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.domain??'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[KinoNewsletter]'
EMAIL_USE_LOCALTIME = False
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'geheim'
EMAIL_HOST_USER = 'newsletter@DOMAIN?'
DEFAULT_FROM_EMAIL = 'Kinoxyz <newsletter@xyz.de'

# https://pypi.org/project/django-maintenance-mode/

# passenger-config restart-app
MAINTENANCE_MODE = None # None True
# if True admin site will not be affected by the maintenance-mode page
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = False
