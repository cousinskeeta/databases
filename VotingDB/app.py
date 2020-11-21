from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from helper_functions import salt_password
from flask_bcrypt import Bcrypt
from tests import new_user_test
from config import DevelopmentConfig
from flask_migrate import Migrate

# from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrage = Migrate()



class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    posts = db.relationship('Posts', backref="owner", uselist=True)
    posts_liked = db.relationship("Posts", )
        
    def p_likes():
        return Post.query.join(post_likes, (PostLikes.c.user_id == id))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Posts(db.Model):
    __tablename__ = 'Posts'
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(120), nullable=False)
    content         = db.Column(db.Text, nullable=False)
    owner_id        = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    date_created    = db.Column(db.DateTime, default= datetime.utcnow)
    user_likes      = db.relationship('post_likes', backref=db.backref('posts', lazy='joined'),
                                 lazy='dynamic', cascade='all', uselist=True)
    def u_likes():
        return User.query.join(post_likes, (post_likes.post_id == id))
    
    def __init__(self, title, content, owner_id):
        self.title      = title
        self.content    = content
        self.owner_id   = owner_id

class post_likes(db.Model):
    __tablename__   = 'post_likes'
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('Users.id'), primary_key=True),
    post_id        = db.Column(db.Integer, db.ForeignKey('Posts.post_id'), primary_key=True),
    date_created    = db.Column(db.DateTime, default= datetime.utcnow, nullable=False)



# PostLikes = db.Table('post_likes',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#     db.Column('owner_id', db.Integer, db.ForeignKey('posts.owner_id'), primary_key=True),
#     created = db.Column(db.DateTime, default= datetime.utcnow)
# )

@app.route('/')
def index():
    # return data points to populate card header, title, body
    popular = None #query for most liked post
    all_posts = None # query all post and orderby date so latest post on top
    return render_template('index.html', all_posts = all_posts, popular = popular)

@app.route('/add_post', methods=['GET','POST'])
def add_post():
    if request.method == 'GET':
        # add condition if query successful
        _user = "" # query current user
        return render_template('/add_post.html', _user = _user)
        # else:
        #     flash('Please login to create post')
        #     print('error loading')
        #     return redirect("/") # create login page and routes
    elif request.method == 'POST':
        _title = request.form['title']
        _content = request.form['content']
        _user = request.form['user']

        try:
            new_post = Posts(title = _title,
                        content = _content,
                        user_id = _user)
            db.session.add(new_post)
            db.session.commit()
            flash('Your Post was Created Successfully!')
            return redirect("/")
        except:
            flash('Sorry. There was an error creating your post. Please try again')
            return render_template('add_post.html', user = _user)
    return render_template('/add_post.html', _user = " ")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":

        new_user_test(request, db, Users)

        _username = request.form['username']
        _email = request.form['email']
        _password = request.form['password']

        salted_pass = salt_password(_password)
        hashed_pass = bcrypt.generate_password_hash(salted_pass)

        try:
            new = Users(username = _username,
                        email = _email,
                        password = hashed_pass)
            db.session.add(new)
            db.session.commit()
            flash('Your account was created successfully!')
            return redirect("/")
        except:
            flash('Sorry. There was an error. Please try again')
            return render_template('auth/reg.html')

    return render_template('auth/reg.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


