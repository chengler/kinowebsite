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

### reqirements collectstatic runserver media


- 




