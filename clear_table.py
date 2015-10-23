#!/usr/bin/python
import MySQLdb
import json
import sys


__author__ = 'bust3r'


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


def table_clear(database):
    cursor = database.cursor()
    combined = 'Combined'
    conversation = 'Conversation'
    packet = 'Packet'
    pcap = 'Pcap'

    cursor.execute('DROP TABLE IF EXISTS Combined, Conversation, Packet, Pcap;')
    cursor.execute('CREATE TABLE IF NOT EXISTS Pcap ('
                   'id VARCHAR(255),'
                   'timegenerated INT,'
                   'PRIMARY KEY (id)'
                   ');')
    cursor.execute('CREATE TABLE IF NOT EXISTS Conversation ('
                   'pcapid VARCHAR(255),'
                   'seqwindow INT DEFAULT 0,'
                   'src VARCHAR(15) DEFAULT NULL,'
                   'dst VARCHAR(15) DEFAULT NULL,'
                   'len INT DEFAULT 0,'
                   'FOREIGN KEY (pcapid) REFERENCES Pcap(id),'
                   'PRIMARY KEY (pcapid, seqwindow)'
                   ');')
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
    cursor.close()
    print 'All tables truncated!'


def main(argv):


    # connect to db
    db = connect_database()
    if not db:
        print 'database connection failed!'
        exit(1)

    # create tables
    table_clear(db)


    # close connection
    db.close()


if __name__ == "__main__":
    main(sys.argv[1:])
