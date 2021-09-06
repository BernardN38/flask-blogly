"""Blogly application."""

from flask import Flask,render_template, redirect,request
from models import db, connect_db, pg_user, pg_pwd, User,Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@localhost:5432/blogly_db".format(username=pg_user, password=pg_pwd)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'welcomehomesir'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/create-user')
def create_user_form():
    return render_template('add_user.html')

@app.route('/create-user', methods=['POST'])
def create_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')
    new_user = User(first_name=first_name, last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')


@app.route('/users/<user_id>')
def user_details(user_id):
    user = User.get_user_details(user_id)
    posts = Post.get_user_posts(user_id)
    return render_template('user_details.html', user=user, posts=posts)


@app.route('/edit/<user_id>')
def edit_user(user_id):
    user = User.get_user_details(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/edit/<user_id>', methods=['POST'])
def edit_user_db(user_id):
    user = User.get_user_details(user_id)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url')
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/users/<user_id>/posts/new')
def new_post_form(user_id):
    user = User.get_user_details(user_id)
    posts = Post.get_user_posts(user_id)
    return render_template('new_post.html',post=posts, user=user)

@app.route('/users/<user_id>/posts/new', methods=["POST"])
def new_post_add(user_id):
    user = User.get_user_details(user_id)
    title = request.form.get('title')
    content= request.form.get('content')
    post = Post(title=title,content=content,user=user.id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<post_id>/edit')
def post_edit_form(post_id):
    post = Post.query.get(post_id)
    return render_template('edit_post.html',post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_form_handle(post_id):
    post = Post.query.get(post_id)
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    db.session.add(post)
    db.session.commit()
    return redirect('/')


@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')
