#!/usr/bin/python
import json
import sys
import os
import init_db
from datetime import datetime
from pytz import timezone

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
            cursor.execute(sql, (pcapid, packet['PIN'], convert_time(packet['time']), packet['src'], packet['dest'],
                                 packet['protocol'], packet['length'], packet['Load'])
                           )
            if "tag" in packet:
                tags = packet['tag']
                for type, tag in tags.items():
                    if not tag:
                        continue
                    sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin)" \
                          "SELECT DISTINCT Tag.tagid, %s, %s " \
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
    sql = "SELECT DISTINCT Tag.tagid, Tag.tag, Tag.type " \
          "FROM Tag, Tagged, Packet " \
          "WHERE Tag.tagid = Tagged.tagid " \
          "AND Tagged.pcapid = Packet.pcapid " \
          "AND Tagged.pin = Packet.pin " \
          "AND NOT (Packet.pcapid = %s AND Packet.pin = %s) " \
          "AND Tag.type = 'SRC'" \
          "AND Packet.src = %s"
    cursor.execute(sql, (pcapid, pin, src))
    src_tag = ""
    match = cursor.fetchall()
    if len(match) != 0:
        src_tag = match[0]['tag']
    sql = "SELECT DISTINCT Tag.tagid, Tag.tag, Tag.type " \
          "FROM Tag, Tagged, Packet " \
          "WHERE Tag.tagid = Tagged.tagid " \
          "AND Tagged.pcapid = Packet.pcapid " \
          "AND Tagged.pin = Packet.pin " \
          "AND NOT (Packet.pcapid = %s AND Packet.pin = %s) " \
          "AND Tag.type = 'DST'" \
          "AND Packet.dst = %s"
    cursor.execute(sql, (pcapid, pin, dst))
    dst_tag = ""
    match = cursor.fetchall()
    print(match)
    if len(match) != 0:
        print(match[0])
        dst_tag = match[0]['tag']
    print("src:"+src_tag+" dst:"+dst_tag)

    sql = "INSERT IGNORE INTO Tagged (tagid, pcapid, pin) " \
          "SELECT DISTINCT Tagged.tagid, %s, %s " \
          "FROM Tag, Tagged, Packet " \
          "WHERE Tag.tagid = Tagged.tagid " \
          "AND Tagged.pcapid = Packet.pcapid " \
          "AND Tagged.pin = Packet.pin " \
          "AND NOT (Packet.pcapid = %s AND Packet.pin = %s) " \
          "AND ((Tag.type = 'SRC' AND Packet.src = %s) OR (Tag.type = 'DST' AND Packet.dst = %s))"
    cursor.execute(sql, (pcapid, pin, pcapid, pin, src, dst))
    #print('new packet tagged!!')


def convert_time(epoch):
    time = datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S.%f')
    datetime_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    time_utc = timezone('UTC').localize(datetime_obj)
    time_cst = time_utc.astimezone(timezone('America/Chicago'))
    return time_cst.strftime('%Y-%m-%d %H:%M:%S.%f')


def main(argv):
    print("begin importing json to database")

    if not argv[0] or not os.path.isfile(argv[0]):
        print('need existing json file as the argument')
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
    pcaptime = convert_time(packets[0]['time'])

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

    os.remove(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
