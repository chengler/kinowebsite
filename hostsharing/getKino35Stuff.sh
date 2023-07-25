#!/bin/bash

# hole die localen Datein der Website, die nicht im git sind, weil sie direkt zum Projekt gehören

cd .
# weil sie für jede Website angepasst werden sollten
echo ##################################
echo scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/mysite/privat_settings.py ../mysite/
scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/mysite/privat_settings.py ../mysite/
echo ##################################
echo scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/mysite/newsletter_keys.py../mysite/
scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/mysite/newsletter_keys.py ../mysite/
echo ##################################
echo scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/db.sqlite3 ../.
scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/db.sqlite3 ../.
echo ##################################
# scp -i ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/static/lokal/* ../static/lokal/
echo rsync -rv --delete -e "ssh -i  ~/.ssh/id_rsa" kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/static/lokal/ ../static/lokal/
rsync -rv --delete -e "ssh -i  ~/.ssh/id_rsa" kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/static/lokal/ ../static/lokal/
echo ##################################
# scp -ri ~/.ssh/id_rsa kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/media/CACHE/images/filme/* ../media/CACHE/images/filme/
echo rsync -rv --delete -e "ssh -i  ~/.ssh/id_rsa" kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/media/CACHE/images/filme/ ../media/CACHE/images/filme/
rsync -rv --delete -e "ssh -i  ~/.ssh/id_rsa" kkf00-kino35.de@kkf00.hostsharing.net:~/kinowebsite/media/CACHE/images/filme/ ../media/CACHE/images/filme/
echo ##################################

