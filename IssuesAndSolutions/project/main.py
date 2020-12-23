from flask import Blueprint, render_template, request, redirect, url_for
# from flask_login import login_required, current_user
from flask_security.decorators import login_required
from flask_security import current_user
from .models import Post, User, Likes, Dislikes, Comments
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
	return render_template('index.html')

@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
	try:
		user_posts = Post.query.filter_by(user_id=current_user.id).all()
	except:
		user_posts = ""

	return render_template('profile.html', current =current_user, user_id = current_user.id, 
	usr_posts=user_posts, Likes=Likes, Dislikes=Dislikes, Comments = Comments, Users=User, all_posts = Post)

@main.route('/edit', methods=['GET','POST'])
@login_required
def edit():
	user_profile = User.query.filter_by(id=current_user.id).first()
	if request.method == 'POST':
		try:
			user_profile.name = request.form.get('name')
			user_profile.email = request.form.get('email')
			user_profile.image = request.form.get('image')
			db.session.commit()
			return redirect(url_for('main.profile'))
		except:
			return redirect(url_for('main.profile'))
	return render_template('edit.html', current=current_user)



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

@main.route('/update_post', methods=['POST'])
@login_required
def update_post():
	post_id = request.form['post_id']
	posts = Post.query.filter_by(id=post_id).first()
	posts.title = request.form.get('title')
	posts.body = request.form.get('body')
	db.session.commit()

	return redirect(url_for('main.profile'))


@main.route('/like_post', methods=['POST'])
@login_required
def like_post():
	user_id = current_user.id
	post_id = request.form['post_id']
	post_like_by_user = Likes(post_id=post_id, user_id=user_id)

	try: 
		db.session.add(post_like_by_user)
		db.session.commit()

	except:
		return redirect(request.referrer)

	return redirect(request.referrer)

@main.route('/dislike_post', methods=['POST'])
@login_required
def dislike_post():
	user_id = current_user.id
	post_id = request.form['post_id']
	post_dislike_by_user = Dislikes(post_id=post_id, user_id=user_id)

	try:
		db.session.add(post_dislike_by_user)
		db.session.commit()
	except:
		return redirect(request.referrer)

	return redirect(request.referrer)


@main.route('/comment', methods=['POST'])
@login_required
def comment():
	body = request.form.get('body')
	user_id = current_user.id
	post_id = request.form['post_id']
	comment_by_user = Comments(body=body, post_id=post_id, user_id=user_id)
	db.session.add(comment_by_user)
	db.session.commit()

	return redirect(request.referrer)

@main.route('/delete_comment', methods=['POST'])
@login_required
def delete_comment():
	comment_id = int(request.form.get('comment_id'))
	print(comment_id)
	comment_to_delete = Comments.query.filter_by(id=comment_id).first()
	print(comment_to_delete)
	try: 
		print('FIRST - connecting to DB')
		db.session.delete(comment_to_delete)
		print('SECOND - comment deleted')
		db.session.commit()
		print('FINAL - database updated')
		return redirect(request.referrer)
	except:
		print("Error occured while deleting comment")
		return redirect(request.referrer)
	return redirect(request.referrer)

@main.route('/delete_post', methods=['GET','POST'])
@login_required
def delete_post():
	if request.method == 'POST':
		post_id = int(request.form['post_id'])
		post_to_delete = Post.query.filter_by(id=post_id).first()
		print(post_to_delete)
		comments_to_delete = Comments.query.filter_by(post_id=post_id).all()
		print(comments_to_delete)
		try: 
			print('FIRST: deleting affiliated comments')
			for i in comments_to_delete:
				db.session.delete(i)
			print('DONE: affiliated comments deleted \n SECOND: Deleting POST')
			db.session.delete(post_to_delete)
			print('DONE: post deleted \n Saving changes to database')
			db.session.commit()
			print('UPDATED: db has been updated')
			return redirect(request.referrer)
		except:
			print("Error occured while deleting post")
			return redirect(request.referrer)
	else:
		return redirect(request.referrer)

@main.route('/discover')
@login_required
def discover():
	all_posts = Post.query.all()
	return render_template('discover.html', all_posts = all_posts, Likes = Likes, Dislikes = Dislikes, 
	current =current_user, user_id = current_user.id, Comments = Comments, Users=User)

@main.route('/post/<id>', methods=['GET','POST'])
@login_required
def post(id):
	posts = Post.query.filter_by(id=id).all()
	return render_template('post.html', current =current_user, user_id = current_user.id, usr_posts=posts, 
	Likes=Likes, Dislikes=Dislikes, Comments = Comments, Users=User, all_posts = Post)