from flask import render_template, flash, redirect, request
from app import app
from flask.ext.mysqldb import MySQLdb
from forms import PacketForm, TagForm, PacketCaptureForm
from werkzeug import secure_filename
from flask.json import jsonify
import json
import os

__author__ = "Donald Cha"
basedir = os.path.abspath(os.path.dirname(__file__))

class Database:

	host = '127.0.0.1'
	user = 'sniffydb_dev'
	password = 'sniffy+DB'
	db = 'sniffydb_main'

	def __init__(self):
		self.connection = MySQLdb.connect(self.host, self.user, 		self.password, self.db)
		self.cursor = self.connection.cursor()

	def execute(self, query):
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

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Network Admin'}
	return render_template('index.html', title='Home', user=user)

@app.route('/data_viz')
def data_viz():
	return render_template('data_viz.html', title="Data Viz")

@app.route('/add_page', methods=['GET', 'POST'])
def add_page():
	form = TagForm()
	pcapid = request.args['pcapid']
	pin = request.args['pin']

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('add_page.html', form=form)
		else:
			db = Database()
			tag = form.tag.data
			type_val = form.type_val.data
			try:
				query = """INSERT INTO Tag (tag, type) VALUES (%s, %s)""" %  ("'"+tag+"'", "'"+type_val+"'")
				db.execute(query)
				print query
				query = """SELECT tagid FROM Tag WHERE tag=%s AND type=%s""" % ("'"+tag+"'", "'"+type_val+"'")
				cur = db.query(query)
				print query
				query = """INSERT INTO Tagged (pcapid, pin, tagid) VALUES (%s, %s, %s)""" %  ("'"+pcapid+"'", pin, cur[0]['tagid'])

				db.execute(query)
				flash('Data Added.')
				return redirect('/view_page')
			except:
				flash('An Error has occured')
				return render_template('add_page.html', form=form)

	elif request.method == 'GET':
		return render_template('add_page.html', form=form)

@app.route('/edit_page', methods=['GET', 'POST'])
def edit_page():
	form = TagForm()
	pcapid = request.args['pcapid']
	pin = request.args['pin']

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('edit_page.html', form=form)
		else:
			db = Database()
			tag = form.tag.data
			type_val = form.type_val.data
			try:
				query = """SELECT tagid FROM Tagged WHERE pcapid=%s AND pin=%s""" % ("'"+pcapid+"'", pin)
				cur = db.query(query)
				if len(cur) == 0:
					flash('Data does not exist')
				else:
					query = """UPDATE Tag SET tag=%s, type=%s WHERE tagid=%s""" %  ("'"+tag+"'", "'"+type_val+"'", cur[0]['tagid'])
					db.execute(query)
					flash('Data editted.')

				return redirect('/view_page')
			except:
				flash('An Error has occured')
				return render_template('edit_page.html', form=form)

	elif request.method == 'GET':
		return render_template('edit_page.html', form=form)

@app.route('/delete_page', methods=['GET', 'POST'])
def delete_page():
	form = TagForm()
	pcapid = request.args['pcapid']
	pin = request.args['pin']
	db = Database()

	try:
		query = """SELECT tagid FROM Tagged WHERE pcapid=%s AND pin=%s""" % ("'"+pcapid+"'", pin)
		cur = db.query(query)
		if len(cur) == 0:
			return redirect('/view_page')
		else:
			query = """DELETE FROM Tag WHERE tagid=%s""" %  (cur[0]['tagid'])
			db.execute(query)
			query = """DELETE FROM Tagged WHERE tagid=%s""" %  (cur[0]['tagid'])
			db.execute(query)
	except:
		flash('An Error has occured')
		return render_template('edit_page.html', form=form)

	return redirect('/view_page')

@app.route('/view_page', methods=['GET'])
def view_page():
	db = Database()
	cur = db.query("""SELECT dst, src, protocol, packettime, pin, pcapid FROM Packet""")
	entries = []
	
	for row in cur:
		temp = dict(dst=row['dst'],
			src=row['src'],
			protocol=row['protocol'],
			pcapid=row['pcapid'],
			packettime=row['packettime'],
			PIN=row['pin'])
		tag_query = """SELECT tag FROM Packet P, Tag T, Tagged Tg WHERE P.pcapid=Tg.pcapid AND P.pin=Tg.pin AND T.tagid=Tg.tagid AND P.pcapid=%s AND P.pin=%s""" % ("'"+row['pcapid']+"'", row['pin'])		
		new_cur = db.query(tag_query)
		if len(new_cur) == 0:
			temp['tag'] = ''
		else:
			temp['tag'] = new_cur[0]['tag']
		entries.append(temp)
	return render_template('view_page.html', entries=entries)

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload
@app.route('/upload', methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		# Check if the file is one of the allowed types/extensions
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			os.system(basedir+"/../../pcap2db.sh " + filename)
	return render_template('upload_page.html')

# Route that will get all entries from mysql database
@app.route('/PCAP', methods=['GET'])
def pcap():
	db = Database()
	cur = db.query("""SELECT * FROM Packet""")
	entries = [dict(dst=row['dst'],
			src=row['src'],
			proto=row['protocol'],
			length=row['len'],
			payload=row['payload'],
			time=row['packettime'],
			PcapID=row['pcapid'],
			PIN=row['pin']) for row in cur]
	return json.dumps(entries)

# Route that will return all IP addresses from mysql database
@app.route('/SHOWIP', methods=['GET'])
def showip():
	db = Database()
	cur = db.query("""SELECT DISTINCT(src) FROM Packet""")
	entries = [dict(src=row['src']) for row in cur]
	return json.dumps(entries)

# Route that will return all IP addresses that a given IP address communicated
@app.route('/COMMUNICATE', methods=['GET'])
def show_communicate():
	ip_address = request.args['ip']
	db = Database()
	query_val = """SELECT DISTINCT dst, protocol FROM Packet WHERE src = %s""" % ("'"+ip_address+"'")
	cur = db.query(query_val) 
	entries = [dict(dst=row['dst'], proto=row['protocol']) for row in cur]
	return json.dumps(entries)

# Route that will clear the data table in mysql database
@app.route('/CLEAR', methods=['GET'])
def clear_table():
	db = Database()
	query_val = """DELETE FROM Packet WHERE (pcapid, pin) NOT IN (SELECT T.pcapid, T.pin FROM Tagged T)"""
	db.execute(query_val) 
	return redirect('/index')

