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

## Wiki
[hier geht es zum wiki](https://github.com/chengler/kinowebsite/wiki)



