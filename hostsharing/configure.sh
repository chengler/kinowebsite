#!/bin/bash
# bei der domain dev.kino35.de sind folgende Schritte notwendig
clear
echo "VORSICHT! bitte prüfen Sie erst das Skript"
echo "Keine Garantie!"


DOMAIN=dev.kino35.de
PAKETUSER=kkf00
if [[ -z $1  ]]; then DOMAIN=$1
if [[ -z $2  ]]; then PACKETUSER=$2
if [[ -z $3  ]]; then USER=DOMAIN # bestpractis bei Hostsharing


echo Vorgabe für user $USER @ Domain $DOMAIN im Paket $PACKETUSER

# exit 0

cd .
echo ergänze die .htaccess in ~/$DOMAIN/.htaccess
echo löschen Sie überflüssiges von Hand!

echo PassengerFriendlyErrorPages on >> ~/$DOMAIN/
echo PassengerPython /home/pacs/$PACKETUSER/users/$USER/pythonenv/bin/python >> ~/$DOMAIN/
echo SetEnv PYTHONPATH /home/pacs/$PACKETUSER/users/$USER/kinowebsite >> ~/$DOMAIN/
echo Die .htaccess findet sich unter ~/$DOMAIN/.htaccess
echo
echo lösche überflüssiges soweit vorhanden
rm -rv ~/doms/$DOMAIN/subs/www/
rm -rv ~/doms/$DOMAIN/subs-ssl/www/
rm -v   ~/doms/$DOMAIN/htdocs-ssl/.htaccess
echo !! in ~/doms/$DOMAIN/htdocs-ssl/.htaccess sollte ein redirect auf die subdomain stehen. z.B.
echo dies wird nicht vom Skript erledigt!
echo  Redirect permanent / https://dev.kino35.de/
echo  

echo die Ordner static und media werden im 'DEBUG = False' direkt vom Webserver ausgeliefert
ln -vs ~/kinowebsite/static ~/doms/$DOMAIN/htdocs-ssl/
ln -vs ~/kinowebsite/media ~/doms/$DOMAIN/htdocs-ssl/
echo

cp -v app-ssl/passenger_wsgi.py ~/doms/$DOMAIN/app-ssl/
echo !! nach einer Änderung am Code muss die Passenger-App neu gestartet werden, damit die Änderungen wirksam werden
echo # passenger-config restart-app


echo Ihre Installation sollte nun unter https://$DOMAIN ereichbar sein.
echo Überprüfen Sie aber erst  ~/doms/$DOMAIN/htdocs-ssl/.htaccess
echo sie sollte mit: "PassengerFriendlyErrorPages on" beginnen
echo Im Produktivem Betreib mit: "PassengerFriendlyErrorPages off"
