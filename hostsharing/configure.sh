#!/bin/bash
# bei der domain www.kino35.de sind folgende Schritte notwendig

DOMAIN=dev.kino35.de
DOMAIN=$1
clear
echo Konfiguriere für DOMAIN $DOMAIN

cd .

echo PassengerFriendlyErrorPages on > ~/doms/$DOMAIN/.htaccess
echo PassengerPython /home/pacs/kkf00/users/$DOMAIN/pythonenv/bin/python3 >> ~/doms/$DOMAIN/.htaccess
echo SetEnv PYTHONPATH /home/pacs/kkf00/users/$DOMAIN/kinowebsite >> ~/doms/$DOMAIN/.htaccess
echo  "~/doms/$DOMAIN/.htaccess wurde erstellt"


 rm -rv ~/doms/$DOMAIN/subs/www/
 rm -rv ~/doms/$DOMAIN/subs-ssl/www/
 rm -v   ~/doms/$DOMAIN/htdocs/.htaccess
 rm -v   ~/doms/$DOMAIN/htdocs-ssl/.htaccess

ln -vs ~/kinowebsite/static ~/doms/$DOMAIN/htdocs-ssl/

cp -v app-ssl/passenger_wsgi.py ~/doms/$DOMAIN/app-ssl/

echo Ihre Installation sollte nun unter https://$DOMAIN ereichbar sein.
