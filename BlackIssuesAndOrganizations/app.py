from flask import Flask, render_template, url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "BlackP0w3r"

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)

class ORGS(db.Model):
	__tablename__ = 'ORGS'
	id = db.Column(db.Integer, primary_key=True)
	zipcode = db.Column(db.Text)
	company = db.Column(db.Text)
	contact = db.Column(db.Text)
	email = db.Column(db.Text)
	website = db.Column(db.Text)
  
	def __init__(self, zipcode, company, contact, email, website, **kwargs):
		self.zipcode = zipcode
		self.company = company
		self.contact = contact
		self.email = email
		self.website = website

	def __repr__(self):
			return '<Zipcode {}>'.format(self.zipcode)  

class ISSUES(db.Model):
	__tablename__ = 'ISSUES'
	id = db.Column("id", db.Integer, primary_key=True)
	zipcode = db.Column(db.Text)
	issue1 = db.Column(db.Text)
	issue2 = db.Column(db.Text)
	issue3 = db.Column(db.Text)
	date = db.Column(db.Text)

	def __init__(self, zipcode, issue1, issue2, issue3, date, **kwargs):
		self.zipcode = zipcode
		self.issue1 = issue1
		self.issue2 = issue2
		self.issue3 = issue3
		self.date = date

	def __repr__(self):
			return '<Zipcode {}>'.format(self.zipcode)   

@app.route('/', methods=["GET", "POST"])
@app.route('/show_all', methods=["GET", "POST"])
def show_all():
	return render_template("index.html", idb = ISSUES.query.all(), orgs_ = ORGS.query.all())

@app.route('/new', methods=["GET", "POST"])
def new():
	if request.method == "POST":
		if not request.form['zipcode'] or not request.form['issue1']:
			flash('Please enter your zipcode and at least ONE issue')
		else:
			today = date.today()
			issue = ISSUES(request.form['zipcode'], request.form['issue1'], 
			request.form['issue2'], request.form['issue3'], today.strftime("%m/%d/%Y"))

			db.session.add(issue)
			db.session.commit()

			flash('Issue was recorded successfully!')
			return redirect(url_for('show_all'))
	return render_template("new.html")

@app.route('/org', methods=["GET"])
def org():
	print('test')
	return render_template("org.html", orgs_ = ORGS.query.all())

@app.route('/new_org', methods=["GET", "POST"])
def new_org():
	if request.method == "POST":
		if not request.form['zipcode'] or not request.form['company']:
			flash('Please enter your zipcode and your company name')
		else:
			org = ORGS(request.form['zipcode'], request.form['company'], 
			request.form['contact'], request.form['email'], request.form['website'])

			db.session.add(org)
			db.session.commit()

			flash('Organization was recorded successfully!')
			return redirect(url_for('show_all'))
	return render_template("new_org.html")

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)