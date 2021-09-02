"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
 

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