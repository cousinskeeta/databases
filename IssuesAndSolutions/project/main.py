from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Likes, Dislikes
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	try:
		user_posts = Post.query.filter_by(user_id=current_user.id).all()
	except:
		user_posts = ""
	return render_template('profile.html', name =current_user.name, user_id = current_user.id, usr_posts=user_posts, Likes=Likes, Dislikes=Dislikes)

@main.route('/create_post', methods=['POST'])
@login_required
def create_post():
	title = request.form.get('title')
	body = request.form.get('body')
	user_id = current_user.id
	author = current_user.name

	new_posts = Post(title=title, body=body, user_id=user_id, author = author)
	
	db.session.add(new_posts)
	db.session.commit()

	return redirect(url_for('main.profile'))

@main.route('/like_post', methods=['POST'])
@login_required
def like_post():
	user_id = current_user.id
	post_id = request.form['post_id']
	post_like_by_user = Likes(post_id=post_id, user_id=user_id)

	db.session.add(post_like_by_user)
	db.session.commit()

	return redirect(request.referrer)

@main.route('/dislike_post', methods=['POST'])
@login_required
def dislike_post():
	user_id = current_user.id
	post_id = request.form['post_id']
	post_dislike_by_user = Dislikes(post_id=post_id, user_id=user_id)

	db.session.add(post_dislike_by_user)
	db.session.commit()

	return redirect(request.referrer)
	
@main.route('/discover')
@login_required
def discover():
	all_posts = Post.query.all()
	return render_template('discover.html', all_posts = all_posts, Likes = Likes, Dislikes = Dislikes)