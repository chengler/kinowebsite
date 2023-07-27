cd .
echo kopiere default Logo und Favicon <= durch eigene ersetzen
copy -v ..\static\lokal\favicon-default.ico ..\static\lokal\favicon.ico
copy -v ..\static\lokal\logo-default.png  ..\static\lokal\KinoLogo.png
echo kopiere newsletter_keys und privat_settings.py
copy -v ..\mysite\configure_newsletter_keys.py ..\mysite\newsletter_keys.py
copy -v ..\mysite\configure_privat_settings.py ..\mysite\privat_settings.py
cd ..\mysite
echo ######
echo 'privat_settings.py' und 'newsletter_keys' müssen angepasst werden!
