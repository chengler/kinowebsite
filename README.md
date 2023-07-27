## Kinowebsite ist 
eine Website für ein kleines Arthouse Kino mit folgenden Kernfunktionen:
- verwaltet Newsletter Abonenten DSVGO konform
- versendet automatisierte newsletter
- Kennt unterschiedliche Kategorien wie z.B Kinderfilme
- Hat einen integrierten Workflow zur Programmfindung. Filme werden
  - vorgeschlagen
  - bewertet
  - fürs Programm ausgewählt
  - freigegeben (Abklärung der Vorführrechte / Vollständigkeit der Infos)
- verwaltet Dienste wie Theke, Kasse, Vorführender
- hält ein Filmarchiv gezeigter und nicht gezeigter Filme
  
Der Flow basiert auf eine ehrenamtlich Struktur und kennt wenig Hirachie:
- Es gibt nur zwei Rollen: Mitarbeitende und Admin.
- Der Admin verwaltet Mitarbeitende
- Die Mitarbeitenden machen alles andere
- Zum versenden manueller Newsletters benötigen Mitarbeitende 'Keys'. Diese sind in `newsletter_keys` hinterlegt

## und basiert auf
- Django Framework <= aktuell Django 4.2 auf Python 3.11

Im folgenden findet sich die Anleitung zur Installation einer Entwicklungsumgebung auf einem Lokalen Windows und einer Produktiven Installation auf einem debian/linux server von hostsharing.net (passenger / wsgi).

# Voraussetzungen zur Installation
Die empfohlene Dateistruktur besteht aus einem Hauptverzeichnis mit zwei Unterverzeichnissen
- `Hauptverzeichnis`
    - `pyvenv` # die virtuelle Python Umgebung
    - `kinowebseite` # das Django/Python Projekt
      
## `pyvenv` enthält Python 3.11 als virtuelle Umgebung
### pyvenv unter win 11
1. Installation
    -  Python 3.11 über den Windows Store installieren
    - `python3.11.exe --version` bestätigt die erfolgreiche Installation
    - Im `Hauptverzeichniss` installiert `python3.11.exe -m venv pyvenv`die virtuelle Umgebung
2. Aktivierung
    - Aus dem `Hauptverzeichnis`aktiviert `.\pyvenv\Scripts\Activate.ps1` die virtuelle Umgebung
    - Sollte die PowerShell dies verhindern, ermöglich `Set-ExecutionPolicy Unrestricted -Scope Process` die Aktivierung.

### pyvenv unter debian linux
1. Installation
    - Folgende [Anleitung](https://wiki.hostsharing.net/index.php?title=Eigenes_Python_installieren) zeigt die Installation auf einem server von hostsharing.net. Wähle die Version 3.11.
    - `python –version` bestätigt die erfolgreiche Installation
    - Im `Hauptverzeichnis` installiert `virtualenv -p python ./pyvenv`die virtuelle Umgebung
2. Aktivierung
    - Aus dem `Hauptverzeichnis`aktiviert `source ./pyvenv/bin/activate` die virtuelle Umgebung
  
## Die `kinowebseite` mit dem Code aus Github erstellen
HINWEIS: Der Code ist nicht vollständig. Mehr Infos unter dem [Issue #16](https://github.com/chengler/kinowebsite/issues/16)
- Es fehlen 
    - die Datenbank # Diese würde z.B. die Newsletterabonenten enthalten
    - das Logo und das Favicon des jeweiligen Kinos # Sind je Kino individuell zu lösen
    - die Filmdatenbank
    - `.gitignore` zeigt dies recht genau

### Clonen unter win 11 oder debian linux
1. Ins `Hauptverzeichnis` wechseln
2. `git clone git@github.com:/chengler/kinowebsite` ausführen
3. die Daten befinden sich nun im Verzeichnis `kinowebseite`
   

### anpassen der setting.py
Die sensiblen Daten aus `settings.py` sind in zwei Dateien ausgegliedert. Diese können wie folgt angelegt werden:
- in den Ordner `kinowebseite/mysite`wechseln
- `cp configure_newsletter_keys newsletter_keys` # Dort sind die Keys um Newsletters zu versenden
- `cp configure_privat_settings.py privat_settings.py` # Debug Mode, Log Level, Maintenance Mode, Credentials zum Mailserver usw.
Anschließend werden die Daten im Editor der Wahl an die lokale Installation angepasst.
- DEBUG = True
- ALLOWED_HOSTS = enthält ['127.0.0.1']
- SECRET_KEY = !


### letzte Schritte der Installation
in der Shell im `Hauptverzeichnis` werden nun folgende Befehle abgesetzt
- python -m pip install --upgrade pip # instaliert die aktuele Version des Installationswerkzeuges pip
- pip install -r requirements.txt     # installiert die benötigten Dajngo Module 
- reqirements collectstatic runserver media
- python manage.py runserver # startet den testserver

In einer lokalen Installation sollte nun der Testserver unter [127.0.0.1:8000](http://127.0.0.1:8000/) ereichbar sein

### Deployment am Beispiel hostsharing.net
Wechseln Sie in den Ordner `kinoserver/hostsharing`. Dort finden sich Skripte, welche das deployen vereinfachen. 
`cat configure.sh ` gibt die Datei aus. Der Aufruf für die Website unter 'dev.beispieldomain.de' wäre 
`./configure.sh dev.beispieldomain.de xyz00
`. Folgende Schritte werden ausgeführt, bzw. müssen händisch erledigt werden:
- ~/doms/$DOMAIN/.htaccess <= wird um die Einstellungen für die Passenger App erweitert.
    -  `PassengerFriendlyErrorPages` `on` für die Produkitvsite und `off` für die Testsite
    -  Diese Datei wäre auch der Ort, um einen [Verzeichnissschutz](https://wiki.hostsharing.net/index.php?title=.htaccess#Passwortschutz_f.C3.BCr_Dateien) anzulegen.
    -  die alten Einträge werden nicht gelöscht <= auf Richtigkeit überprüfen
- ~/doms/$DOMAIN/htdocs-ssl/ <= erhält die symbolischen links, damit der Webserver statische Datein ausliefern kann
    - in `privat_settings.py` muss dafür DEBUG=False stehen
    - Da statischen Dateien werden wie folgt erstellt:
        - `Kinowebsite$` `python manage.py collectstatic` 
 - die `passenger_wsgi.py` wird an die richtige Stelle kopiert um vom Webserver ausgeführt zu werden.
-  ~/doms/$DOMAIN/htdocs-ssl/.htaccess <= Diese Datei sollte existieren und auf die verwendete Subdomain wie  'www'oder  'dev'verweisen

## eigenes Repository starten
Es benötigt einen Account auf Github. Ein Beitrag zum Code ist über Passwort nicht mehr möglich, sondern nur noch über Keys. Hier erfolgt nun eine sehr einfache Anleitung, welche viele Möglichkeiten nicht berücksichtigt.
Es lohnt sich den Schlüssel mit einem Passort zu sichern. So gibt es einmal ein 'sehr schweres' Passwort an der 'GitHub Pforte' und ein 'leichtes' am lokalen Rechner. So ist, wenn der Schlüßel verschwindet noch nicht alles verloren.
### ssh Zugang
Dafür benötigt es eine shell. z.B. die bash unter Linux oder die Power-Shell unter Windows
- `ls ~/.ssh` <= gibt es bereits einen Schlüßel, also die `id_rsa.pub`
    - falls nein: `ssh-keygen.exe -t rsa -b 4096 -C EMAIL-ADRESSE`
- den `id_rsa.pub` bei Settings >> SSH and PGP  hochladen
- den SSH-Agent starten
      - `ssh-agent.exe ` (Win)
      - `eval "$(ssh-agent -s)" `(linux)
- `ssh-add ~/.ssh/id_rsa` <= Schlüssel hinzufügen

### git konfiguieren 
- `git config --global user.name "GIT-USER-NAME"`
- `git config --global user.email phu@examole.de`

### git verwenden
- `git branch -M main`
- `git push git@github.com:/chengler/kinowebsite`



