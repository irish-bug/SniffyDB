from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired

__author__ = "Donald Cha"

class PacketForm(Form):
	src = StringField('Source IP', validators=[DataRequired()])	
	dst = StringField('Destination IP', validators=[DataRequired()])
	protocol = IntegerField('Protocol', validators=[DataRequired()])
	length = IntegerField('Packet Length', validators=[DataRequired()])
	payload = StringField('Payload', validators=[DataRequired()])
	packettime = StringField('Packet Time', validators=[DataRequired()])
	pcapid = StringField('PcapID', validators=[DataRequired()])
	pin = IntegerField('PIN', validators=[DataRequired()])
	submit = SubmitField("Send")

class TagForm(Form):
	tag = StringField('Tag', validators=[DataRequired()])
	type_val = SelectField('Type', choices=[('DST', 'Destination IP'), ('SRC', 'Source IP')])
	submit = SubmitField("Submit")

class PacketCaptureForm(Form):
	pcapid = StringField('PcapID', validators=[DataRequired()])
	pcaptime = StringField('Pcap Generation Time', validators=[DataRequired()])
	submit = SubmitField("Submit")
