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
        cursor.execute(sql, (pcap['pcapid'], pcap['pcaptime']))
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
            auto_tag(cursor, pcapid, packet)
    connection.commit()
    print('new packets added!')


def auto_tag(cursor, pcapid, packet):
    pin = packet['PIN']
    dst = packet['dest']
    src = packet['src']

    sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin)" \
          "SELECT Tagged.tagid, %s, %s " \
          "FROM Tagged, Packet " \
          "WHERE Tagged.pin = Packet.pin " \
          "AND Tagged.pcapid = Packet.pcapid " \
          "AND (Packet.src = %s OR Packet.dst = %s)"
    cursor.execute(sql, (pcapid, pin, dst, dst))
    cursor.execute(sql, (pcapid, pin, src, src))
    print('new packet tagged!!')


def main(argv):
    print("begin importing json to database")

    if not argv[0]:
        print('need json file as the argument')
        exit(1)

    # load json
    pcap = json.load(open(argv[0]))

    # save pcapid for later use

    if not pcap['PcapID'] or not pcap['packets']:
        print('input is in unexpected format')
        exit(1)

    p = {}
    p['pcapid'] = pcap['PcapID']
    packets = pcap['Packets']
    p['pcaptime'] = packets[0]['time']

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
    add_pcap(connection, p)
    add_packet(connection, p['pcapid'], packets)

    # close connection
    connection.close()


if __name__ == "__main__":
    main(sys.argv[1:])
