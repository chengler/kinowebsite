# kino-35
thx to: https://tutorial.djangogirls.org 

# hier gehts weiter
https://tutorial.djangogirls.org/de/django_forms/
https://docs.djangoproject.com/en/3.0/intro/tutorial05/

Now let’s update our index view in polls/views.py to use the template:
#
# einmalig
#

# richte virtualenv ein
mkdir djangokino

cd djangokino

#win

python -m venv myvenv 

#linux

python3 -m venv myvenv


# starte venv
#win

myvenv\Scripts\activate

#linux

source myvenv/bin/activate


# git clone
git clone chengler@github.com:/chengler/kino-35

# installiere django
python -m pip install --upgrade pip

pip install -r requirements.txt

#
# Sicherheit
#

lösche superuser cen

änder secret key in mysite/settings.py


#
# Änderung der DB (models.py)
#
python manage.py makemigrations [app]
python manage.py migrate 

#
# immer
#

# starte venv
source myvenv/bin/activate

# starte Entwicklungsserver
python manage.py runserver

# zeichne UML Diagramm
installiere graphviz
https://graphviz.gitlab.io/download/


https://simpleit.rocks/python/django/generate-uml-class-diagrams-from-django-models/
$ python manage.py graph_models -a -o myapp_models.png
$ ./manage.py graph_models -a -g -o my_project_visualized.png

# deployment in update.txt


python3 -m venv myvenv
pip install -r requirements.txt

https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-apache-and-mod_wsgi-on-ubuntu-14-04


was ist nicht im git
privat_settings
newsletter_keys
db.sqlite nur die startversion ohne newsletter mit archiv


optimierung
https://developers.google.com/speed/pagespeed/insights/?url=https%3A%2F%2Ftest.35kino.de
