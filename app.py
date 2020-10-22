from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite://///Users/jacobtadesse/Documents/practice/databases/issues.db'
db = SQLAlchemy(app)

class issues(db.Model):
	__tablename__ = 'issues'
	id = db.Column('id', db.Integer, primary_key=True)
	zip = db.Column('zip', db.String)
	issue1 = db.Column('issue1', db.String)
	issue2 = db.Column('issue2', db.String)
	issue3 = db.Column('issue3', db.String)
	date = db.Column('date', db.String)

	def __init__(self, id, zip, issue1, issue2, issue3, date):
		self.id = id
		self.zip = zip
		self.issue1 = issue1
		self.issue2 = issue2
		self.issue3 = issue3
		self.date = date
