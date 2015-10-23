from flask import render_template, flash, redirect, request
from app import app
from flask.ext.mysqldb import MySQLdb
from forms import SubmitForm, SearchForm, DeleteForm, EditForm
from werkzeug import secure_filename
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

db = Database()

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'Network Admin'}
	return render_template('index.html', title='Home', user=user)



@app.route('/add_page', methods=['GET', 'POST'])
def add_page():
	form = SubmitForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('add_page.html', form=form)
		else:
			dst = form.dst.data
			src = form.src.data
			proto = form.proto.data
			seqwindow = form.seqwindow.data
			length = form.length.data
			payload = form.payload.data
			time = form.time.data
			PcapID = form.PcapID.data
			PIN = form.PIN.data
			try:
				query = """INSERT INTO Combined values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" %  ("'"+PcapID+"'", PIN, "'"+time+"'", seqwindow, "'"+src+"'", "'"+dst+"'", proto, length, "'"+payload+"'")
				db.execute(query)
				flash('Data Added.')
				return redirect('/add_page')
			except:
				flash('An Error has occured')
				return redirect('/index')

	elif request.method == 'GET':
		return render_template('add_page.html', form=form)


@app.route('/view_page', methods=['GET'])
def view_page():
	cur = db.query("""SELECT * FROM Combined""")
	entries = [dict(dst=row['dst'],
			src=row['src'],
			proto=row['protocol'],
			seqwindow=row['seqwindow'],
			length=row['len'],
			payload=row['payload'],
			time=row['packettime'],
			PcapID=row['pcapid'],
			PIN=row['pin']) for row in cur]
	return render_template('view_page.html', entries=entries)

@app.route('/search_page', methods=['GET', 'POST'])
def search_page():
	form = SearchForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('search_page.html', form=form)
		else:
			PcapID = form.PcapID.data
			PIN = form.PIN.data
			try:
				query = """SELECT * FROM Combined WHERE pcapid=%s AND pin=%d""" %  ("'"+PcapID+"'", PIN)
				cur = db.query(query)
				entries = [dict(dst=row['dst'],
				src=row['src'],
				proto=row['protocol'],
				seqwindow=row['seqwindow'],
				length=row['len'],
				payload=row['payload'],
				time=row['packettime'],
				PcapID=row['pcapid'],
				PIN=row['pin']) for row in cur]
				return render_template('search_page.html', form=form, entries=entries)
			except:
				print "Error"
				return redirect('/search_page')

	elif request.method == 'GET':
		return render_template('search_page.html', form=form, entries=None)

@app.route('/delete_page', methods=['GET', 'POST'])
def delete_page():
	form = DeleteForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('delete_page.html', form=form)
		else:
			PcapID = form.PcapID.data
			PIN = form.PIN.data
			try:
				query = """SELECT * FROM Combined WHERE pcapid=%s AND pin=%d""" %  ("'"+PcapID+"'", PIN)
				cur = db.query(query)
				if len(cur) == 0:
					flash('Data does not exist')
				else:
					query = """DELETE FROM Combined WHERE pcapid=%s AND pin=%d""" %  ("'"+PcapID+"'", PIN)
					db.execute(query)
					flash('Data Deleted.')
				return redirect('/delete_page')
			except:
				print "Error"
				return redirect('/delete_page')

	elif request.method == 'GET':
		return render_template('delete_page.html', form=form)

@app.route('/edit_page', methods=['GET', 'POST'])
def edit_page():
	form = EditForm()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('edit_page.html', form=form)
		else:
			PcapID = form.PcapID.data
			PIN = form.PIN.data
			choice = form.select.data
			new_val = form.new_val.data
			if not (choice == 'seqwindow' or choice == 'len' or choie == 'protocol'):
				new_val = "'"+new_val+"'"
			try:
				query = """SELECT * FROM Combined WHERE pcapid=%s AND pin=%d""" %  ("'"+PcapID+"'", PIN)
				cur = db.query(query)
				if len(cur) == 0:
					flash('Data does not exist')
				else:
					query = """UPDATE Combined SET %s=%s WHERE pcapid=%s AND pin=%d""" %  (choice, new_val, "'"+PcapID+"'", PIN)
					db.execute(query)
					flash('Data editted.')
				return redirect('/edit_page')
			except:
				print "Error"
				return redirect('/edit_page')

	elif request.method == 'GET':
		return render_template('edit_page.html', form=form)

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

@app.route('/add')
def add():
	try:
		query = """INSERT INTO Combined values (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" %  ("'1'", "'1'", "'1'", 1, 1, "'1'", "'1'", "'1'", 1)
		db.execute(query)
		return redirect('/index')
	except:
		print "HI"
		return redirect('/index')
