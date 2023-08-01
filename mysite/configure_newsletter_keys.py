# mysite/newsletter_keys.py
### die Keys zum versenden der Newsletter
# kopieren sie in newsletter_keys.py
# wählen sie die werte und
HEUTE_KEY = 'HEUTE'
HINWEIS_KEY = 'GESTERN'
SONDERNEWSLETTER_PIN = 'MORGEN'

# wenn von einer live-Instanz die variablen Dateien wie Datenbank, Filmplakaten in die Entwicklungsumgebungen kopiert werden soll
# hier kommt die Variable rein
# # ziel=<user>@<server_url>:<basedir>
# der # Tag ist gewollt. Die Variable beginnt mit #! und wird mit grep ausgelesen 
#!ZIEL=lege Ziel in ~/kinowebsite/mysite/newsletter_keys.py fest