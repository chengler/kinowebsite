#!/bin/bash
# Dieses Skript kopiert die Varibalent Teile, Datenbank, Filmplakate, der Live Webseite zur jeweiligen Entwicklungsumgebeung
# Damit kann immer mir dem aktuellen Stand entwickelt und getestet werden

# wechsel in das Verzeichniss in dem dieses Skript steht -> hostsharing
dir="$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
cd $dir

#!ZIEL=lege Ziel in ~/kinowebsite/mysite/newsletter_keys.py fest

# ziel=<user>@<server_url>:<basedir>
# lese Variable #!ZIEL aus datei
ziel=$(cat ../mysite/newsletter_keys.py | grep "#!ZIEL" | awk 'BEGIN {FS="="} {print $2}')
echo $ziel

printf "\n"
echo  aktualisiere Grafikdaten ...
rsync -r -e "ssh -i  ~/.ssh/id_rsa" $ziel/media/CACHE/images/filme/ ../media/CACHE/images/filme/
echo Grafikdatein aktualisiert.
echo "Aktualisiere Datenbank ..."
scp -i ~/.ssh/id_rsa $ziel/db.sqlite3 ../.
echo "Datenbank aktualisiert."
