#!/bin/bash
# check argument
if [ -z "$1" ]
    then
    echo "yo i need the filename"
    exit 1
fi

# pcap to json
# sniffy alias for sniffyDB
/home/project/sniffydb/SniffyDB/sniffyDB $1
if [ $? -ne 0 ]; then
    echo "pcap to json parse failed for some reason :("
    exit 1
fi

pcap="pcap.json"

# json to mysql database
# j2d alias for json2db.py
/home/project/sniffydb/SniffyDB/json2db.py $pcap
if [ $? -ne 0 ]; then
    echo "json to database parse failed for some reason :("
fi

# remove json file
rm $pcap
exit 0
