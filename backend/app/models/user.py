import random

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    code = str(int(random.uniform(0, 1) * 1000000))

    def __repr__(self):
        return '<Role %r>' % self.username

    def forgetpass(self):
        codes = str(int(random.uniform(0, 1) * 1000000))
        return codes
