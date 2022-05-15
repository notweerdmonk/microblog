# define fixtures for testing

import pytest
from app import db, create_app
from config import Config
from app.models import User, Post
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta
from flask_wtf.csrf import generate_csrf
from flask import current_app, session

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

@pytest.fixture(scope='module')
def create_new_app():
    return create_app(TestConfig)

@pytest.fixture(scope='module')
def test_client(create_new_app):
    new_app = create_new_app
    new_app_context = new_app.app_context()
    new_app_context.push()
    db.create_all()

    yield new_app.test_client()

    db.session.remove()
    db.drop_all()
    new_app_context.pop()

'''
courtesy: https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
'''
class RequestShim(object):
    """
    A fake request that proxies cookie-related methods to a Flask test client.
    """
    def __init__(self, client):
        self.client = client
        self.vary = set({})

    def set_cookie(self, key, value='', *args, **kwargs):
        "Set the cookie on the Flask test client."
        server_name = current_app.config["SERVER_NAME"] or "localhost"
        return self.client.set_cookie(
            server_name, key=key, value=value, *args, **kwargs)

    def delete_cookie(self, key, *args, **kwargs):
        "Delete the cookie on the Flask test client."
        server_name = current_app.config["SERVER_NAME"] or "localhost"
        return self.client.delete_cookie(
            server_name, key=key, *args, **kwargs)

@pytest.fixture(scope='module')
def request_context(test_client):
    '''
    courtesy: https://gist.github.com/singingwolfboy/2fca1de64950d5dfed72
    '''
    request = RequestShim(test_client)
    environ_overrides = {}
    test_client.cookie_jar.inject_wsgi(environ_overrides)
    with current_app.test_request_context('/auth/login'):
        csrf_token = generate_csrf()
        current_app.session_interface.save_session(
                current_app, session, request)

    yield session, csrf_token

def create_new_users():
    users = []

    user = User(username='Rahul', email='rahul@mail.com',
            password_hash=generate_password_hash('password'))
    users.append(user)

    user = User(username='Simran', email='simran@mail.com',
            password_hash=generate_password_hash('password'))
    users.append(user)

    return users

@pytest.fixture(scope='function')
def new_user():
    return create_new_users()[0]

@pytest.fixture(scope='function')
def add_new_user(test_client, new_user):
    '''
    In case of error the database can contain the test user.
    If so delete the user first.
    '''
    user_from_db =\
        db.session.query(User).filter_by(username=new_user.username).first()
    if user_from_db is not None:
        db.session.delete(user_from_db)
        db.session.commit()

    db.session.add(new_user)
    db.session.commit()

    user_from_db = User.query.filter_by(username=new_user.username).first()
    yield user_from_db

    db.session.delete(user_from_db)
    db.session.commit()

def create_new_posts(user):
    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0)

    posts = []

    post = Post(timestamp=timestamp, body='Flask is awesome.', author=user)
    posts.append(post)

    post = Post(timestamp=timestamp, body='Python is awesome.', author=user)
    posts.append(post)

    return posts

@pytest.fixture(scope='function')
def new_post(new_user):
    new_post = create_new_posts(new_user)[0]
    return new_user, new_post

@pytest.fixture(scope='function')
def add_new_post(test_client, new_user):
    user = new_user

    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0)
    post = Post(timestamp=timestamp, body='Flask is awesome.', author=user)

    '''
    In case of error the database can contain the test user and post.
    If so delete the user and post first.
    '''
    user_from_db =\
        db.session.query(User).filter_by(username=user.username).first()
    if user_from_db is not None:
        post_from_db =\
            db.session.query(Post).filter_by(author=user_from_db).first()
        if post_from_db is not None:
            db.session.delete(post_from_db)
        db.session.delete(user_from_db)
        db.session.commit()

    db.session.add(user)
    db.session.add(post)
    db.session.commit()

    user_from_db = User.query.filter_by(username=user.username).first()
    if user_from_db is not None:
        post_from_db = Post.query.filter_by(author=user_from_db).first()

    yield user_from_db, post_from_db

    db.session.delete(post_from_db)
    db.session.delete(user_from_db)
    db.session.commit()

@pytest.fixture(scope='module')
def follow_user():
    new_users = create_new_users()
    user1 = new_users[0]
    user2 = new_users[1]

    user_from_db =\
        db.session.query(User).filter_by(username=user1.username).first()
    if user_from_db is None:
        db.session.add(user1)
    else:
        user1 = user_from_db
    user_from_db =\
        db.session.query(User).filter_by(username=user2.username).first()
    if user_from_db is None:
        db.session.add(user2)
    else:
        user2 = user_from_db

    new_posts = create_new_posts(new_users[0])
    db.session.add(new_posts[0])
    db.session.add(new_posts[1])

    db.session.commit()

    user1.follow(user2)
    db.session.commit()

    yield user1, user2, new_posts

    db.session.delete(new_posts[0])
    db.session.delete(new_posts[1])
    db.session.delete(user1)
    db.session.delete(user2)
    db.session.commit()

@pytest.fixture(scope='module')
def unfollow_user(follow_user):
    user1, user2, _ = follow_user

    user1 =\
        db.session.query(User).filter_by(username=user1.username).first()
    user2 =\
        db.session.query(User).filter_by(username=user2.username).first()

    user1.unfollow(user2)
    db.session.commit()

    yield user1, user2
