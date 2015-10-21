from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextField
from wtforms.validators import DataRequired

class SubmitForm(Form):
	src = StringField('src', validators=[DataRequired()])	
	dst = StringField('dst', validators=[DataRequired()])
	proto = StringField('proto', validators=[DataRequired()])
	seqwindow = IntegerField('seqwindow', validators=[DataRequired()])
	length = IntegerField('length', validators=[DataRequired()])
	payload = StringField('payload', validators=[DataRequired()])
	time = StringField('time', validators=[DataRequired()])
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
							('proto', 'Protocol'), ('seqwindow', 'Sequence Window'),
							('length', 'Packet Length'), ('payload', 'Payload'),
							('time', 'Timestamp')])
	new_val = TextField('New Value', validators=[DataRequired()])
	submit = SubmitField("Send")
