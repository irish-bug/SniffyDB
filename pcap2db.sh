#!/bin/bash

if [ -z "$1" ]
    then
    echo "yo i need the filename"
    exit 1
fi

./sniffyDB $1

pcap="test"
head $pcap
# replace test with pcap.json when everything is ready

./json2db.py $pcap
