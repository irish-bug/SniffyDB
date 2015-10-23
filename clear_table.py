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


def table_clear(database, pcapid, packets):
    cursor = database.cursor()

    cursor.execute('TRUNCATE TABLE Combined;')
    database.commit()
    cursor.close()
    print 'Combined table truncated!'


def main(argv):


    # connect to db
    db = connect_database()
    if not db:
        print 'database connection failed!'
        exit(1)

    # create tables
    table_clear(db, PcapID, Packets)


    # close connection
    db.close()


if __name__ == "__main__":
    main(sys.argv[1:])
