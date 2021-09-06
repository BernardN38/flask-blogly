"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 

pg_user = "tester"
pg_pwd = "testing123"

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app) 



class User(db.Model):
    __tablename__ = 'users'

    @classmethod
    def get_user_details(cls, user_id):
       return cls.query.filter_by(id=user_id).one()

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column (
        db.String(20),
        nullable=False
    )
    last_name = db.Column (
        db.String(20),
        nullable=False
    )
    image_url = db.Column(
        db.String(2048),
        nullable=True
    )


class Post(db.Model):
    __tablename__ = 'posts'
    
    @classmethod
    def get_user_posts(cls, user_id):
       return cls.query.filter_by(user=user_id).all()

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column (
        db.String(30),
        nullable=False
    )
    content = db.Column (
        db.String(300),
        nullable=False
    )
    created_at = db.Column (
        db.Text,
        default=datetime.now(),
        nullable=False,
    )
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
