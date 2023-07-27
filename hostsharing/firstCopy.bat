cls
echo off
echo "bitte folgende vier Dateien von Hand kopieren"
echo copy -v '..\static\lokal\favicon-default.ico' '..\static\lokal\favicon.ico'
echo copy -v ..\static\lokal\logo-default.png  ..\static\lokal\KinoLogo.png
echo copy -v ..\mysite\configure_newsletter_keys.py ..\mysite\newsletter_keys.py
echo copy -v ..\mysite\configure_privat_settings.py ..\mysite\privat_settings.py
echo "'privat_settings.py' und 'newsletter_keys' anpassen!"
echo on
