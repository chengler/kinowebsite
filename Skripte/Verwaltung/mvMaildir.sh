#!/bin/bash
# Skript für hostsharing.net managed Webserver
# Für den Packetadmin
# GPL
# kopiere Mailbox von pacs (SSD) auf storage (HDD) und setze link von pacs auf storage

PACKET=$(cut -d "-" -f 1 <<< $USER)
NAME=$(cut -d "-" -f 2 <<< $USER)
# printf "User %s in Packet %s\n" $NAME $PACKET
if [[ ! -d /home/storage/$PACKET/users/$NAME/Maildir && -d /home/pacs/$PACKET/users/$NAME/Maildir ]]
    then
        mv /home/pacs/$PACKET/users/$NAME/Maildir /home/storage/$PACKET/users/$NAME/
        ln -s /home/storage/$PACKET/users/$NAME/Maildir /home/pacs/$PACKET/users/$NAME/
fi
printf "\nDer neue link zum Postfach:"
ls -l /home/pacs/$PACKET/users/$NAME/