from flask import render_template, redirect, url_for, request, flash # Blueprint
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, logout_user, login_required
from flask_security import, Blueprint, hash_password, login_required, login_user, logout_user, SQLAlchemyUserDatastore, ch
from flask_security.utils import verify_password
from .models import User, Role
from . import db

auth = Blueprint('auth', __name__)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form['email']
	password = request.form['password']
	remember = True if request.form.get('remember') else False
	user = User.query.filter_by(email=email).first()
	if not user or not verify_password(user.password)
	if not user or not check_password_hash(password, user.password):
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login'))

	login_user(user, remember=remember)	
	return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	name = request.form.get('name')
	password = hash_password(request.form.get('password'))

	user = User.query.filter_by(email=email).first()

	if user:
		flash('Email address already exists')
		return redirect(url_for('auth.signup'))

	# new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
	# db.session.add(new_user)

	user_datastore.create_user(
		email = email,
		password = password
	)
	db.session.commit()

	return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.index'))

