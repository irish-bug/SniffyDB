#!/usr/bin/python
import pymysql
import init_db
import json2db


__author__ = 'SimonSK'


def main():
    print("testing with dummy data (dhcp.pcap, pcap2.json")
    msg = "1. tables reset and packets from dhcp.pcap added to the packet table\n" \
          "2. dummy tag (Bob) created on pin=2 packet's SRC (192.168.0.1)\n" \
          "3. add packets from pcap2.json (which is just a slightly modified version of dhcp.pcap)\n" \
          "all packets 192.168.0.1 are automatically tagged with Bob" \
          "Tagged table should have 4 entries."
    init_db.main()
    json2db.main(["../pcaps/dhcp.pcap"])
    print("done")


if __name__ == "__main__":
    main()
