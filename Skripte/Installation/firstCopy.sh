#!/bin/bash
# firstCopy
clear
echo "VORSICHT! bitte prüfen Sie erst das Skript"
echo "Keine Garantie!"
echo kopiert die Dateien welche angepasst werden müssen.

# exit 0

cd .
echo kopiere default Logo und Favicon <= durch eigene ersetzen
cp -v  ../static/lokal/favicon-default.ico  ../static/lokal/favicon.ico
cp -v   ../static/lokal/logo-default.png  ../static/lokal/KinoLogo.png
echo cp kopiere newsletter_keys und privat_settings.py
cp -v ../mysite/configure_newsletter_keys.py ../mysite/newsletter_keys.py # Dort sind die Keys um Newsletters zu versenden
cp -v ../mysite/configure_privat_settings.py ../mysite/privat_settings.py # Debug Mode, Log Level, Maintenance Mode, Credentials zum Mailserver usw. 
cd ../mysite/
echo ######
echo 'privat_settings.py' und 'newsletter_keys' müssen angepasst werden
