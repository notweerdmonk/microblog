from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index = True, unique = True)
    email = db.Column(db.String(32), index = True, unique = True)
    password_hash = db.Column(db.String(32))
    post = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, Email {}>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return \
            'https://gravatar.com/avatar/{}?size={}&default=robohash' \
            .format(digest, size)

class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Date {}, Post {}>'.format(self.timestamp, self.body)
