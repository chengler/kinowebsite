#!/bin/bash
# Skript für hostsharing.net managed Webserver
# GPL
# legt Postfach und E-Mailadresse an.
# ruft skript zum verschieben des maildir Verzeichnisses auf
# erwartet Vor- und Nachname als Input

# Postfach sind die Initialien <Packet>-mail_<Initialien>
# Emailadresse <vorname>.<nachname>@<domain>

domain=kino35.de
if [ ! $domain ]
then
    echo "Es muss noch die Domain im Skript angegeben werden"
    exit 1
fi

# Initialien sind anpassbar, wenn bereits von anderem user verwendet.
# Es wird vor der erstellung überprüft, ob Postfach und E-Mailadresse bereits vorhanden ist.

# 0. hole Input
# 1. Postfach anlegen
# 2. Email Adresse anlegem
# 3. Postfach verschieben
# 4. Hinweis webinterface

# 0. hole Input
printf "\n***\nFür wen soll eine E-Mail Adresse angelegt werden?\nVorname Nachname: "
read Vorname Nachname
vorname=$(echo $Vorname |  tr '[:upper:]' '[:lower:]')
nachname=$(echo $Nachname |  tr '[:upper:]' '[:lower:]')
initialien=$(cut -c 1 <<< $vorname)
initialien+=$(cut -c 1 <<< $nachname)
packetname=$(cut -d "-" -f 1 <<< $USER) # wie xyz00
localpart="${vorname}.${nachname}" # Email vor dem @
user=$packetname"-mail_"$initialien      # PostfachUser  <Packename>-mail_<Initialien>
password=$(openssl rand -base64 8) # Initialpasswort

#  teste ob postfachuser schon exisiert

printf "\nHängt das script hier über 5 Sekunden, ist eine einmalige anmeldung bei hsscript nötig!\n"
printf "In diesem Fall abbrechen und folgenden Befehl absetzen\n"
printf "/usr/local/bin/hsscript --expr \"user.search({where:{name:'%s'}})\"\n\n" $packetname
while :
do
    test_user=$(/usr/local/bin/hsscript --expr "user.search({where:{name:'"$user"'}})")
    test_user=$(echo $test_user | awk -F'name' '{print $2}' )
    if [ ! -z "$test_user" ]
    then # Möglichkeit für andere Initialien
        printf "Postfachuser %s existiert, wir brauchen andere Initialien\n" $user
        read -e -p  "Ändern und mit Enter übernehmen? " -i $initialien Initialien
        initialien=$(echo $Initialien |  tr '[:upper:]' '[:lower:]')
        user=$packetname"-mail_"$initialien      # PostfachUser  <Packename>-mail_<Initialien>
    else
        printf "\nPostfachUser: %s\n" $user
        break
    fi
done

# teste, ob localpart-Adresse schon existiert
test_localpart=$(/usr/local/bin/hsscript --expr "emailaddress.search({where:{domain:'"$domain"', localpart:'"$localpart"'}})")
test_localpart=$(echo $test_localpart | awk -F'localpart' '{print $2}' )
if [ ! -z "$test_localpart" ] # wenn nicht leer, dann
then
    printf "E-Mail user %s@kino35.de existiert, wir brauchen anderen Namen\n" $localpart
    exit 1 # Programmabbruch
else
    printf "E-Mail %s@%s\n\n" $localpart $domain
fi

# 1. Postfach anlegen
/usr/local/bin/hsscript --expr "user.add({set:{name:'"$user"',comment:'Postfach "$Vorname" "$Nachname"',shell:'/usr/bin/passwd',password: '"$password"' }})"
# 2. Email Adresse anlegem
/usr/local/bin/hsscript --expr "emailaddress.add({set:{target:'"$user"',localpart:'"$localpart"',domain:'"$domain"'}})"
# 3. Postfach verschieben
printf "** Verschiebe das neue Postfach von ssd auf Festplatte. user %s" $user
sleep 5 # gebe hs-admin zeit den user anzulegen
sudo -u $user -s /bin/bash  /home/pacs/$packetname/mvMaildir.sh
# 4. Hinweis webinterface
printf "\n*** Jetzt noch im Webmailer Name und E-Mailadresse anpassen\n"
printf "*** Name:           %s %s\n" $Vorname $Nachname
printf "*** E-Mail:         %s@%s\n" $localpart $domain
printf "*** User:           %s\n" $user
printf "*** IntialPassword: %s\n" $password
printf "\nhttps://webmail.hostsharing.net/\n\n"