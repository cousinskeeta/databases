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
	image = db.Column(db.Text, default="https://images-na.ssl-images-amazon.com/images/I/41hBGDoF8eL._AC_.jpg")
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	posts = db.relationship('Post', backref=db.backref('user', lazy='joined'), lazy=True)
	def votes_(self):
		votes_ = db.session.query(Votes).filter(Votes.candidate_id == User.id)
		return votes_
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
	def comments_(self):
		comments_ = db.session.query(Comments).filter(Comments.post_id == Post.id)
		return comments_
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

class Comments(db.Model):
	__tablename__ = 'comments'
	__table_args__ = {'extend_existing': True} 
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	users = db.relationship(User, backref='comments-by-user', foreign_keys=[user_id])
	posts = db.relationship(Post, backref='comments-by-post', foreign_keys=[post_id])

class Groups(db.Model):
	__tablename__ = 'groups'
	__table_args__ ={'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	zipcode = db.Column(db.Integer, nullable=False, unique=True)
	group_name = db.Column(db.Text, nullable=False)
	group_description = db.Column(db.Text, nullable=False)
	owner = db.relationship(User, backref='groups-owned-by-user', foreign_keys=[owner_id])
	
class Candidates(db.Model):
	__tablename__ = 'candidates'
	__table_args__ ={'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	candidate_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
	position = db.Column(db.Text, nullable=False)
	candidate = db.relationship(User, backref='candidate-by-user', foreign_keys=[candidate_id])
	group = db.relationship(Groups, backref='groups-running-by-user', foreign_keys=[group_id])

class Votes(db.Model):
	__tablename__ = 'votes'
	__table_args__ ={'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	create_dttm = db.Column(db.DateTime, default= datetime.utcnow)
	candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
	voter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	candidate = db.relationship(Candidates, backref='candidate-by-userid', foreign_keys=[candidate_id])
	voter = db.relationship(User, backref='votes-by-user', foreign_keys=[voter_id])
