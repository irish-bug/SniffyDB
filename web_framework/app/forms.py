from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired

__author__ = "Donald Cha"

class SubmitForm(Form):
	src = StringField('Source IP', validators=[DataRequired()])	
	dst = StringField('Destination IP', validators=[DataRequired()])
	proto = StringField('Protocol', validators=[DataRequired()])
	seqwindow = IntegerField('Sequence Window', validators=[DataRequired()])
	length = IntegerField('Packet Length', validators=[DataRequired()])
	payload = StringField('Payload', validators=[DataRequired()])
	time = StringField('Packet Time', validators=[DataRequired()])
	PcapID = StringField('PcapID', validators=[DataRequired()])
	PIN = IntegerField('PIN', validators=[DataRequired()])
	submit = SubmitField("Send")

class DeleteForm(Form):
	PcapID = StringField('PcapID', validators=[DataRequired()])
	PIN = IntegerField('PIN', validators=[DataRequired()])
	submit = SubmitField("Send")

class SearchForm(Form):
	PcapID = StringField('PcapID', validators=[DataRequired()])
	PIN = IntegerField('PIN', validators=[DataRequired()])
	submit = SubmitField("Send")

class EditForm(Form):
	PcapID = StringField('PcapID', validators=[DataRequired()])
	PIN = IntegerField('PIN', validators=[DataRequired()])
	select = SelectField('Field to Change', choices=[('src', 'Source IP'), ('dst', 'Destination IP'),
							('protocol', 'Protocol'), ('seqwindow', 'Sequence Window'),
							('len', 'Packet Length'), ('payload', 'Payload'),
							('packettime', 'Packet Time')])
	new_val = TextField('New Value', validators=[DataRequired()])
	submit = SubmitField("Send")
