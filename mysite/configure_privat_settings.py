#  mysite/privat_settings.py
from django.contrib.messages import constants as message_constants
MESSAGE_LEVEL = 10  # DEBUG default 20= Info; 40 Error
#DEBUG = False
DEBUG = True

DJANGO_LOG_LEVEL = 'WARNING'  #  DEBUG, INFO, WARNING, ERROR, CRITICAL. DEBUG Ausgabe in Datei nach settings.py
DJANGO_FORMATTER = 'simple' # logger outpu in simple oder verbose


ALLOWED_HOSTS = [ '127.0.0.1']
DEFAULT_DOMAIN = 'https://Meine.Domain'
SECRET_KEY = 'YOUR_KEY_HERE(_#4g7&iljthr&5!*90#oo%fp!-1(!r%i42&*e<F2>w&@-0@(&bykwgbba'


# https://pypi.org/project/django-maintenance-mode/

# passenger-config restart-app
MAINTENANCE_MODE = None # None True
# if True admin site will not be affected by the maintenance-mode page
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = False

# Frog Key
FROG_SRC = False
# FROG_SRC = "https://embed.eventfrog.de/de/events.html?key= bis zum "

