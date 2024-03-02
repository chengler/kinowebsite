#!/bin/bash
# Dieses Skript kopiert die Varibalent Teile, Datenbank, Filmplakate, der Live Webseite zur jeweiligen Entwicklungsumgebeung
# Damit kann immer mir dem aktuellen Stand entwickelt und getestet werden

# wechsel in das Verzeichniss in dem dieses Skript steht -> 
dir="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd $dir

# von welchem server wird kopiert
ziel=$(cat ../../mysite/produktiver_server.txt)
echo $ziel

printf "\n"
echo  aktualisiere Grafikdaten ...
rsync -r -e "ssh -i  ~/.ssh/id_rsa" $ziel/media/CACHE/images/filme/ ../media/CACHE/images/filme/
echo Grafikdatein aktualisiert.
echo "Aktualisiere Datenbank ..."
scp -i ~/.ssh/id_rsa $ziel/db.sqlite3 ../.
echo "Datenbank aktualisiert."
