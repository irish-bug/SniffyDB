#!/usr/bin/python
import init_db
import json2db
import os


__author__ = 'SimonSK'


def add_tag(connection, tag, type):
    with connection.cursor() as cursor:
        # Insert a row for every packet. ignore if the primary key already exists.
        sql = "INSERT IGNORE INTO Tag (tag, type)" \
              "VALUES (%s, %s)"
        cursor.execute(sql, (tag, type))
        connection.commit()
    print('new tag added!')


def add_tagged(connection, tagid, pcapid, pin):
    with connection.cursor() as cursor:
        # Insert a row for every packet. ignore if the primary key already exists.
        sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin)" \
              "VALUES (%s, %s, %s)"
        cursor.execute(sql, (tagid, pcapid, pin))
        connection.commit()
    print('packet tagged!')


def main():
    print("testing with dummy data (dhcp.pcap, pcap2.json")
    init_db.main()
    os.system("./pcap2db.sh ../pcaps/dhcp.pcap")

    connection = init_db.connect_database()
    add_tag(connection, 'bob', 'SRC')
    add_tag(connection, 'bob', 'DST')
    add_tagged(connection, 1, 'dhcp.pcap', 2)
    connection.close()

    json2db.main(['./pcap2.json'])
    print("finished adding dummy data")

    msg = "1. tables reset and packets from dhcp.pcap added to the packet table\n" \
          "2. dummy tag (Bob) created on pin=2 packet's SRC (192.168.0.1)\n" \
          "3. add packets from pcap2.json (which is just a slightly modified version of dhcp.pcap)\n" \
          "all packets 192.168.0.1 are automatically tagged with Bob\n" \
          "Tagged table should have 4 entries."
    print(msg)


if __name__ == "__main__":
    main()
