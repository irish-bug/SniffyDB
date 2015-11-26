#!/usr/bin/python
import json
import sys
import init_db


__author__ = 'SimonSK'


def add_predefined_tag(connection, key_dict):
    with connection.cursor() as cursor:
        for tag in key_dict.itervalues():
            sql = "INSERT IGNORE INTO Tag (tag, type) " \
                  "VALUES (%s, %s)"
            cursor.execute(sql, (tag, "SRC"))
            cursor.execute(sql, (tag, "DST"))


def add_pcap(connection, pcapid, pcaptime):
    with connection.cursor() as cursor:
        # new pcap entry. ignore if the primary key already exists.
        sql = "INSERT IGNORE INTO PacketCapture (pcapid, pcaptime)" \
              "VALUES (%s, %s)"
        cursor.execute(sql, (pcapid, pcaptime))
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
            if "tag" in packet:
                tags = packet['tag']
                for type, tag in tags.items():
                    sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin)" \
                          "SELECT Tag.tagid, %s, %s " \
                          "FROM Tag " \
                          "WHERE Tag.type = %s AND Tag.tag = %s"
                    cursor.execute(sql, (pcapid, packet['PIN'], type, tag))
            connection.commit()
            auto_tag(cursor, pcapid, packet)
            connection.commit()
    print('new packets added!')


def auto_tag(cursor, pcapid, packet):
    pin = packet['PIN']
    dst = packet['dest']
    src = packet['src']

    sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin)" \
          "SELECT DISTINCT Tagged.tagid, %s, %s " \
          "FROM Tag, Tagged, Packet " \
          "WHERE Tag.type = 'SRC' " \
          "AND Tagged.pin = Packet.pin " \
          "AND Tagged.pcapid = Packet.pcapid " \
          "AND (Packet.src = %s OR Packet.src = %s)"
    cursor.execute(sql, (pcapid, pin, src, dst))
    sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin)" \
          "SELECT DISTINCT Tagged.tagid, %s, %s " \
          "FROM Tag, Tagged, Packet " \
          "WHERE Tag.type = 'DST' " \
          "AND Tagged.pin = Packet.pin " \
          "AND Tagged.pcapid = Packet.pcapid " \
          "AND (Packet.dst = %s OR Packet.dst = %s)"
    cursor.execute(sql, (pcapid, pin, src, dst))
    print('new packet tagged!!')


def main(argv):
    print("begin importing json to database")

    if not argv[0] or argv[0] != "pcap.json":
        print('need json file as the argument')
        exit(1)

    # load json
    pcap = json.load(open(argv[0]))
    # check if json is properly formatted
    if not pcap['PcapID'] or not pcap['Packets']:
        print('input is in unexpected format')
        exit(1)
    # variable for later use
    pcapid = pcap['PcapID'].split('/')[-1]
    packets = pcap['Packets']
    pcaptime = packets[0]['time']

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

    # add predefined tags if the list is provided
    if "Keywords" in pcap:
        key_dict = pcap['Keywords']
        add_predefined_tag(connection, key_dict)

    # add packets
    add_pcap(connection, pcapid, pcaptime)
    add_packet(connection, pcapid, packets)

    # close connection
    connection.close()


if __name__ == "__main__":
    main(sys.argv[1:])
