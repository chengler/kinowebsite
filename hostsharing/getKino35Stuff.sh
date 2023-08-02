#!/bin/bash

# hole die localen Datein der Website, die nicht im git sind, weil sie direkt zum Projekt gehören
# Dies macht erst Sinn, wenn es eine Webseite gibt, welche zur weiterentwicklung geclont werden soll
# Dies macht nur einmal Sinn. zukünftig die Datei etVarData.sh verwenden

echo "erst Skript lesen, anpassen und dann exit 0 auskommentieren"
echo "keine Garantie, sie sollten das Skript verstehen"
# exit 0

# wechsel in das Verzeichniss in dem dieses Skript steht -> hostsharing
dir="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd $dir

# von welchem server wird kopiert
ziel=$(cat ../mysite/produktiver_server.txt)
echo $ziel


# mysite/privat_settings.py
scp -i ~/.ssh/id_rsa $ziel/mysite/privat_settings.py ../mysite/
# mysite/newsletter_keys.py
scp -i ~/.ssh/id_rsa $ziel/mysite/newsletter_keys.py ../mysite/
# db.sqlite3
scp -i ~/.ssh/id_rsa $ziel/db.sqlite3 ../.
# static/lokal/* <- favicon etc.
rsync -r  -e "ssh -i  ~/.ssh/id_rsa" $ziel/static/lokal/ ../static/lokal/
# Filmplakate etc
rsync -r -e "ssh -i  ~/.ssh/id_rsa" $ziel/media/CACHE/images/filme/ ../media/CACHE/images/filme/
rsync -r -e "ssh -i  ~/.ssh/id_rsa" $ziel/media/filme/ ../media/filme/


