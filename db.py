import os

from gino import Gino

db = Gino()

DATABASE_URI = os.getenv('DATABASE_URI')


class User(db.Model):
    __tablename__ = 'my_users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
