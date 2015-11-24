import MySQLdb

__author__ = "Donald Cha"

class Database:

	host = 'localhost'
	user = 'sniffydb_dev'
	password = 'sniffy+DB'
	db = 'sniffydb_main'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, 		self.password, self.db)
		self.cursor = self.connection.cursor()

	def insert(self, query):
		try:
			self.cursor.execute(query)
			self.connection.commit()
		except:
			self.connection.rollback()



	def query(self, query):
		cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
		cursor.execute(query)

		return cursor.fetchall()

	def __del__(self):
		self.connection.close()


if __name__ == "__main__":

	db = Database()
	
	# drop table if it already exists.
	query = """
	DROP TABLE IF EXISTS Packet
	"""
	db.query(query)

	query = """
	DROP TABLE IF EXISTS PacketCapture
	"""
	db.query(query)

	query = """
	DROP TABLE IF EXISTS Tag
	"""
	db.query(query)

	query = """
	DROP TABLE IF EXISTS Tagged
	"""
	db.query(query)

	# Create table
	query = """
	CREATE TABLE IF NOT EXISTS Packet (pcapid VARCHAR(255), pin INT, packettime VARCHAR(255) NOT NULL, src VARCHAR(15) DEFAULT NULL, dst VARCHAR(15) DEFAULT NULL, protocol INT DEFAULT -1, len INT DEFAULT 0, payload VARCHAR(2000) DEFAULT NULL, PRIMARY KEY (pcapid, pin));
	"""

	db.query(query)

	query = """
	CREATE TABLE IF NOT EXISTS PacketCapture (pcapid VARCHAR(255), pcaptime VARCHAR(255) NOT NULL, PRIMARY KEY (pcapid));
	"""

	db.query(query)

	query = """
	CREATE TABLE IF NOT EXISTS Tag (tagid INT NOT NULL AUTO_INCREMENT, tag VARCHAR(255) NOT NULL, type VARCHAR(3) DEFAULT "SRC", PRIMARY KEY (tagid));
	"""

	db.query(query)

	query = """
	CREATE TABLE IF NOT EXISTS Tagged (pcapid VARCHAR(255), pin INT, tagid INT, PRIMARY KEY (pcapid, pin, tagid));
	"""

	db.query(query)

