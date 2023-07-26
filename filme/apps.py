from django.apps import AppConfig


class FilmeConfig(AppConfig):
    name = 'filme'

# änderung bei django update 
# https://docs.djangoproject.com/en/3.2/releases/3.2/
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'