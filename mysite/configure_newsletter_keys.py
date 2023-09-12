# unbedingt ändern
SECRET_KEY = 'YOUR_KEY_HERE(_#4g7&iljthr&5!*90#oo%fp!-1(!r%i42&*e<F2>w&@-0@(&bykwgbba'

# mysite/newsletter_keys.py
### die Keys zum versenden der Newsletter
# kopieren sie in newsletter_keys.py
# wählen sie die werte und
HEUTE_KEY = 'HEUTE'
HINWEIS_KEY = 'GESTERN'
SONDERNEWSLETTER_PIN = 'MORGEN'

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



