#!/usr/bin/python
import pymysql


__author__ = 'SimonSK'


host = '127.0.0.1'
user = 'sniffydb_dev'
password = 'sniffy+DB'
db = 'sniffydb_main'


def connect_database():
    try:
        connection = pymysql.connect(host, user, password, db)
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
            return connection
    except pymysql.Error:
        print('could not connect to the database')
    return None


def clear_all(connection):
    with connection.cursor() as cursor:
        sql = "DROP TABLE IF EXISTS Tagged, Tag, Packet, PacketCapture;"
        cursor.execute(sql)
        connection.commit()
    print('All tables dropped!')


def create_pcap(connection):
    with connection.cursor() as cursor:
        # create a new table if not already exists
        sql = "CREATE TABLE IF NOT EXISTS PacketCapture (" \
              "pcapid VARCHAR(255) NOT NULL ," \
              "pcaptime REAL DEFAULT 0," \
              "PRIMARY KEY (pcapid)" \
              ")"
        cursor.execute(sql)
        connection.commit()
    print('PacketCapture table created!')


def create_packet(connection):
    with connection.cursor() as cursor:
        # create a new table if not already exists
        # packettime TIMESTAMP(6)
        sql = "CREATE TABLE IF NOT EXISTS  Packet (" \
              "pcapid VARCHAR(255) NOT NULL," \
              "pin INT NOT NULL," \
              "packettime REAL DEFAULT 0," \
              "src VARCHAR(15) DEFAULT NULL," \
              "dst VARCHAR(15) DEFAULT NULL," \
              "protocol INT DEFAULT -1," \
              "len INT DEFAULT 0," \
              "payload VARCHAR(2000) DEFAULT NULL," \
              "FOREIGN KEY (pcapid) REFERENCES PacketCapture(pcapid)" \
              "ON DELETE CASCADE ON UPDATE CASCADE," \
              "PRIMARY KEY (pcapid, pin)" \
              ")"
        cursor.execute(sql)
        connection.commit()
    print('Packet table created!')


def create_tag(connection):
    with connection.cursor() as cursor:
        # create a new table if not already exists
        sql = "CREATE TABLE IF NOT EXISTS Tag (" \
              "tagid INT NOT NULL AUTO_INCREMENT," \
              "tag VARCHAR(255) NOT NULL," \
              "type VARCHAR(3) NOT NULL," \
              "PRIMARY KEY (tagid)" \
              "UNIQUE (tag, type)" \
              ")"
        cursor.execute(sql)
        connection.commit()
    print('Tag table created!')


def create_tagged(connection):
    with connection.cursor() as cursor:
        # create a new table if not already exists
        sql = "CREATE TABLE IF NOT EXISTS Tagged (" \
              "tagid INT NOT NULL AUTO_INCREMENT," \
              "pcapid VARCHAR(255) NOT NULL," \
              "pin INT NOT NULL," \
              "FOREIGN KEY (pcapid, pin) REFERENCES Packet(pcapid, pin)" \
              "ON UPDATE CASCADE ON DELETE CASCADE," \
              "FOREIGN KEY (tagid) REFERENCES Tag(tagid)" \
              "ON UPDATE CASCADE ON DELETE CASCADE" \
              ")"
        cursor.execute(sql)
        connection.commit()
    print('Tagged table created!')


def main():
    print("begin initializing tables")

    # connect to db
    connection = connect_database()
    if not connection:
        print('database connection failed!')
        exit(1)

    # clear all existing tables
    clear_all(connection)

    # create tables
    create_pcap(connection)
    create_packet(connection)
    create_tag(connection)
    create_tagged(connection)

    # close connection
    connection.close()


if __name__ == "__main__":
    main()
