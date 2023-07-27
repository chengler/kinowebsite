#!/bin/bash
# firstCopy
clear
echo "VORSICHT! bitte prüfen Sie erst das Skript"
echo "Keine Garantie!"

# exit 0

cd .
echo ##################################################
echo kopiere default Logo und Favicon <= durch eigene ersetzen
cp -v ..\static\lokal\favicon-default.ico ..\static\lokal\favicon.ico
cp -v ..\static\lokal\logo-default.png  ..\static\lokal\KinoLogo.png
echo ###################################################
echo kopiere newsletter_keys und privat_settings.py
cp -v ..\mysite\configure_newsletter_keys.py ..\mysite\newsletter_keys.py
cp -v ..\mysite\configure_privat_settings.py ..\mysite\privat_settings.py
echo fertig
