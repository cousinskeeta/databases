from flask import Flask, render_template, url_for, flash, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:////Users/jacobtadesse/Documents/practice/databases/issues.db'
app.config['SECRET_KEY'] = "BlackP0w3r"


db = SQLAlchemy(app)

class issues(db.Model):
	__tablename__ = 'issues'
	id = db.Column("id", db.Integer, primary_key=True)
	zipcode = db.Column(db.String(7))
	issue1 = db.Column(db.String(240))
	issue2 = db.Column(db.String(240))
	issue3 = db.Column(db.String(240))
	date = db.Column(db.String(10))

	def __init__(self, zipcode, issue1, issue2, issue3, date, **kwargs):
		# self.id = id
		self.zipcode = zipcode
		self.issue1 = issue1
		self.issue2 = issue2
		self.issue3 = issue3
		self.date = date

@app.route('/')
def show_all():
	return render_template("index.html", idb = issues.query.all())

@app.route('/new', methods=["GET", "POST"])
def new():
	if request.method == "POST":
		if not request.form['zipcode'] or not request.form['issue1']:
			flash('Please enter your zipcode and at least ONE issue')
		else:
			today = date.today()
			issue = issues(request.form['zipcode'], request.form['issue1'], 
			request.form['issue2'], request.form['issue3'], today.strftime("%m/%d/%Y"))

			db.session.add(issue)
			db.session.commit()

			flash('Issue was recorded successfully!')
			return redirect(url_for('show_all'))
	return render_template("new.html")

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)