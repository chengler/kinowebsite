#!/bin/bash
# Dieses Skript kopiert die Varibalent Teile, Datenbank, Filmplakate, der Live Webseite zur jeweiligen Entwicklungsumgebeung
# Damit kann immer mir dem aktuellen Stand entwickelt und getestet werden

# wechsel in das Verzeichniss in dem dieses Skript steht ->
dir="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
echo "dir="$dir
cd $dir

# von welchem server wird kopiert
ziel=$(cat ../../mysite/produktiver_server.txt)
echo "ziel="$ziel

printf "\n"
echo "Aktualisiere Datenbank ..."
scp -i ~/.ssh/id_rsa $ziel:~/kinowebsite/db.sqlite3  ~/kinowebsite/
echo "Datenbank aktualisiert."

printf "\n"
echo Hole Thumbnails # auch deakt
 rsync -z -v -r -e "ssh -i ~/.ssh/id_rsa" $ziel:~/kinowebsite/media/CACHE/* ~/kinowebsite/media/CACHE/
echo Hole Plakate
rsync -z -v -r -e "ssh -i ~/.ssh/id_rsa" $ziel:~/kinowebsite/media/filme/plakate/* ~/kinowebsite/media/filme/plakate/
kkf00-dev.kino35.de@h94:~/kinowebsite/Skripte/Installation$