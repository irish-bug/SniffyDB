#!/bin/bash

if [ -z "$1" ]
    then
    echo "yo i need the filename"
    exit 1
fi

./sniffyDB $1

pcap="pcap.json"

./json2db.py $pcap
