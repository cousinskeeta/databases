from flask_login import UserMixin
from datetime import datetime
from . import db

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100), unique=True)
	name = db.Column(db.String(1000))
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	posts = db.relationship('Post', backref=db.backref('user', lazy='joined'), lazy=True)

	def __repr__(self):
		return '<User %r>' % self.email


class Post(db.Model):
	__tablename__ = 'post'
	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	body = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(100), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	def likes_(self):
		likes_ = db.session.query(Likes).filter(Likes.post_id == Post.id)
		return likes_
	def dislikes_(self):
		dislikes_ = db.session.query(Dislikes).filter(Dislikes.post_id == Post.id)
		return dislikes_
	# likes = db.relationship("User", secondary="likes", backref='post', lazy='dynamic')   #backref=db.backref('likes', lazy="dynamic")

class Likes(db.Model):
	__tablename__ = 'likes'
	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	users = db.relationship(User, backref='likes-by-user', foreign_keys=[user_id])
	posts = db.relationship(Post, backref='likes-by-post', foreign_keys=[post_id])

class Dislikes(db.Model):
	__tablename__ = 'dislikes'
	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	users = db.relationship(User, backref='dislikes-by-user', foreign_keys=[user_id])
	posts = db.relationship(Post, backref='dislikes-by-post', foreign_keys=[post_id])