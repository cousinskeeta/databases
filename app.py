from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////Users/jacobtadesse/Documents/practice/databases/issues.db'
db = SQLAlchemy(app)

class issues(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	zipcode = db.Column(db.String(7))
	issue1 = db.Column(db.String(240))
	issue2 = db.Column(db.String(240))
	issue3 = db.Column(db.String(240))
	date = db.Column(db.String(10))

	def __init__(self, zipcode, issue1, issue2, issue3, date):
		# self.id = id
		self.zipcode = zipcode
		self.issue1 = issue1
		self.issue2 = issue2
		self.issue3 = issue3
		self.date = date
