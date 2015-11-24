#!/usr/bin/python
import json
import sys
import init_db


__author__ = 'SimonSK'


def add_pcap(connection, pcap):
    with connection.cursor() as cursor:
        # new pcap entry. ignore if the primary key already exists.
        sql = "INSERT IGNORE INTO Pcap (pcapid, pcaptime)" \
              "VALUES (%s, %s)"
        cursor.execute(sql, (pcap['id'], pcap['time']))
    connection.commit()
    print('new pcap added!')


def add_packet(connection, pcapid, packets):
    with connection.cursor() as cursor:
        # Insert a row for every packet. ignore if the primary key already exists.
        for packet in packets:
            sql = "INSERT IGNORE INTO Packet (pcapid, pin, packettime, src, dst, protocol, len, payload)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (pcapid, packet['PIN'], packet['time'], packet['src'], packet['dest'],
                                 packet['protocol'], packet['length'], packet['Load'])
                           )
    connection.commit()
    print('new packets added!')


def apply_tag(database, pcapid, packets):
    cursor = database.cursor()
    print('Combined table updated!')


def main(argv):
    print("begin importing json to database")

    if not argv[0]:
        print('need json file as the argument')
        exit(1)

    # load json
    pcap = json.load(open(argv[0]))

    # save pcapid for later use
    pcapid = pcap['PcapID']

    packets = pcap['Packets']

    if not pcapid or not packets:
        print('input is in unexpected format')
        exit(1)

    # connect to db
    connection = init_db.connect_database()
    if not connection:
        print('database connection failed!')
        exit(1)

    # check tables
    init_db.create_pcap(connection)
    init_db.create_packet(connection)
    init_db.create_tag(connection)
    init_db.create_tagged(connection)

    # create tables
    add_pcap(connection, pcapid)
    add_packet(connection, pcapid, packets)

    # close connection
    connection.close()


if __name__ == "__main__":
    main(sys.argv[1:])
