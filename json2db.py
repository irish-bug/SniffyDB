#!/usr/bin/python
import MySQLdb
import json
import sys


__author__ = 'SimonSK'


dialect = 'mysql'
user = 'sniffydb_dev'
passwd = 'sniffy+DB'
server = '127.0.0.1'
database = 'sniffydb_main'


def connect_database():
    try:
        db = MySQLdb.connect(server, user, passwd, database)
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        results = cursor.fetchone()
        # Check if anything at all is returned
        if not results:
            print 'seems connected, but there is nothing in it'
        return db
    except MySQLdb.Error:
        print 'could not connect to the database'
    return None


def table_pcap(database, pcapid):
    cursor = database.cursor()

    # create a new table if not already exists
    cursor.execute('CREATE TABLE IF NOT EXISTS Pcap ('
                   'id VARCHAR(255),'
                   'timegenerated INT,'
                   'PRIMARY KEY (id)'
                   ');')
    database.commit()

    # Insert a row for every packet. ignore if the primary key already exists.
    cursor.execute('INSERT IGNORE INTO Pcap (id, timegenerated)'
                   'values (%s, %s);',
                   (pcapid, None))
    database.commit()
    cursor.close()
    print 'Pcap table updated!'


def table_conversation(database, pcapid, packets):
    cursor = database.cursor()

    # create a new table if not already exists
    cursor.execute('CREATE TABLE IF NOT EXISTS Conversation ('
                   'pcapid VARCHAR(255),'
                   'seqwindow INT,'
                   'src VARCHAR(15) DEFAULT NULL,'
                   'dst VARCHAR(15) DEFAULT NULL,'
                   'len INT DEFAULT 0,'
                   'FOREIGN KEY (pcapid) REFERENCES Pcap(id),'
                   'PRIMARY KEY (pcapid, seqwindow)'
                   ');')
    database.commit()

    # Insert a row for every packet. ignore if the primary key already exists.
    for packet in packets:
        cursor.execute('INSERT IGNORE INTO Conversation (pcapid, seqwindow, src, dst, len)'
                       'VALUES (%s, %s, %s, %s, %s);',
                       (pcapid, packet['seq-window'], packet['src'], packet['dest'], packet['length']))
        database.commit()
    cursor.close()
    print 'Conversation table updated!'


def table_packet(database, pcapid, packets):
    cursor = database.cursor()

    # create a new table if not already exists
    cursor.execute('CREATE TABLE IF NOT EXISTS Packet ('
                   'pcapid VARCHAR(255),'
                   'pin INT,'
#                   'packettime TIMESTAMP(6),'
                   'packettime VARCHAR(255) NOT NULL,'
                   'protocol INT DEFAULT -1,'
                   'payload VARCHAR(2000) DEFAULT NULL,'
                   'FOREIGN KEY (pcapid) REFERENCES Pcap(id),'
                   'PRIMARY KEY (pcapid, pin)'
                   ');')
    database.commit()

    # Insert a row for every packet. ignore if the primary key already exists.
    for packet in packets:
        cursor.execute('INSERT IGNORE INTO Packet (pcapid, pin, packettime, protocol, payload)'
#                       'VALUES (%s, %s, FROM_UNIXTIME(%s), %s, %s);',
                       'VALUES (%s, %s, %s, %s, %s);',
                       (pcapid, packet['PIN'], packet['time'], packet['protocol'], packet['Load']))
        database.commit()
    cursor.close()
    print 'Packet table updated!'


def table_combined(database, pcapid, packets):
    cursor = database.cursor()

    # create a new table if not already exists
    cursor.execute('CREATE TABLE IF NOT EXISTS Combined ('
                   'pcapid VARCHAR(255),'
                   'pin INT,'
                   'packettime VARCHAR(255) NOT NULL,'
                   'seqwindow INT DEFAULT -1,'
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
    print 'Combined table updated!'


def main(argv):
    # load json
    if not argv[0]:
        print 'need json file as the argument'
        exit(1)
    pcap = json.load(open(argv[0]))

    # save pcapid for later use
    PcapID = pcap['PcapID']

    Packets = pcap['Packets']

    if not PcapID or not Packets:
        print 'input is in unexpected format'
        exit(1)

    # connect to db
    db = connect_database()
    if not db:
        print 'database connection failed!'
        exit(1)

    # create tables
    table_combined(db, PcapID, Packets)
    table_pcap(db, PcapID)
    table_conversation(db, PcapID, Packets)
    table_packet(db, PcapID, Packets)

    # close connection
    db.close()


if __name__ == "__main__":
    main(sys.argv[1:])