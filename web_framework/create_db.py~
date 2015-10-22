import MySQLdb

__author__ = "Donald Cha"

class Database:

	host = 'localhost'
	user = 'root'
	password = ''
	db = 'testdb'

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

	#CleanUp Operation
	#del_query = "DELETE FROM basic_python_database"
	#db.insert(del_query)

	# Create table
	query = """
	CREATE TABLE pcap (dst VARCHAR(15), src VARCHAR(15), proto VARCHAR(100) DEFAULT 'UNKNOWN', seqwindow INT(100), length INT(100), payload VARCHAR(2000) DEFAULT 'NONE', time VARCHAR(100), PcapID VARCHAR(100), PIN INT(100), PRIMARY KEY (PcapID, PIN));
	"""

	db.query(query)
	#db.insert(query)

	# Data retrieved from the table
	#select_query = """
	#SELECT * FROM basic_python_database
	#WHERE age = 21
	#"""

	#people = db.query(select_query)

	#for person in people:
	#print "Found %s " % person['name']
