"""Blogly application."""

from flask import Flask,render_template, redirect,request
from models import db, connect_db, pg_user, pg_pwd, User
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
    return render_template('user_details.html', user=user)


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
