#!/usr/bin/python
import pymysql
import json
import sys


__author__ = 'SimonSK'


host = '127.0.0.1'
user = 'sniffydb_dev'
password = 'sniffy+DB'
database = 'sniffydb_main'
charset = 'utf8mb4'


def connect_database():
    try:
        connection = pymysql.connect(host, user, password, database, charset)
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT VERSION()')
                result = cursor.fetchone()
            # Check if anything at all is returned
            if not result:
                print('seems connected, but there is nothing in it')
            else:
                print('connected. fetched following %s' % result)
        finally:
            connection.close()
    except pymysql.Error:
        print('could not connect to the database')
    return None


def add_pcap(connection, pcap):
    with connection.cursor() as cursor:
        # create a new table if not already exists
        sql = "CREATE TABLE IF NOT EXISTS Pcap (" \
              "pcapid VARCHAR(255)," \
              "pcaptime REAL DEFAULT 0," \
              "PRIMARY KEY (pcapid)" \
              ")"
        cursor.execute(sql)
    connection.commit()

    with connection.cursor() as cursor:
        # new pcap entry. ignore if the primary key already exists.
        sql = "INSERT IGNORE INTO Pcap (pcapid, pcaptime)" \
              "VALUES (%s, %s)"
        cursor.execute(sql, (pcap['id'], pcap['time']))
    connection.commit()
    print('Pcap table updated!')


def add_packet(connection, pcapid, packets):
    with connection.cursor() as cursor:
        # create a new table if not already exists
        # packettime TIMESTAMP(6)
        sql = "CREATE TABLE IF NOT EXISTS  Packet (" \
              "pcapid VARCHAR(255)," \
              "pin INT," \
              "packettime REAL DEFAULT 0," \
              "src VARCHAR(15) DEFAULT NULL," \
              "dst VARCHAR(15) DEFAULT NULL," \
              "protocol INT DEFAULT -1," \
              "len INT DEFAULT 0," \
              "payload VARCHAR(2000) DEFAULT NULL," \
              "FOREIGN KEY (pcapid) REFERENCES Pcap(pcapid)," \
              "PRIMARY KEY (pcapid, pin)" \
              ")"
        cursor.execute(sql)
    connection.commit()

    with connection.cursor() as cursor:
        # Insert a row for every packet. ignore if the primary key already exists.
        for packet in packets:
            sql = "INSERT IGNORE INTO Packet (pcapid, pin, packettime, src, dst, protocol, len, payload)" \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (pcapid, packet['PIN'], packet['time'], packet['src'], packet['dest'],
                                 packet['protocol'], packet['length'], packet['Load'])
                           )
    connection.commit()
    print('Packet table updated!')


def add_tag(database, pcapid, packets):
    cursor = database.cursor()

    # create a new table if not already exists
    cursor.execute('CREATE TABLE IF NOT EXISTS Combined ('
                   'pcapid VARCHAR(255),'
                   'pin INT,'
                   'packettime VARCHAR(255) NOT NULL,'
                   'seqwindow INT DEFAULT 0,'
                   'src VARCHAR(15) DEFAULT NULL,'
                   'dst VARCHAR(15) DEFAULT NULL,'
                   'protocol INT DEFAULT -1,'
                   'len INT DEFAULT 0,'
                   'payload VARCHAR(2000) DEFAULT NULL,'
                   'PRIMARY KEY (pcapid, pin)'
                   ');')
    database.commit()

    # Insert a row for every packet. ignore if the primary key already exists.
    for packet in packets:
        cursor.execute('INSERT IGNORE INTO Combined (pcapid, pin, packettime, seqwindow, src, dst, protocol, len, payload)'
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);',
                       (pcapid, packet['PIN'], packet['time'], packet['seq-window'], packet['src'], packet['dest'], packet['protocol'], packet['length'], packet['Load']))
        database.commit()
    cursor.close()
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
    connection = connect_database()
    if not connection:
        print('database connection failed!')
        exit(1)

    # create tables
    table_combined(db, PcapID, Packets)
    create_pcap(db, PcapID)
    table_conversation(db, PcapID, Packets)
    table_packet(db, PcapID, Packets)

    # close connection
    db.close()


if __name__ == "__main__":
    main(sys.argv[1:])
