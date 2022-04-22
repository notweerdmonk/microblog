# define fixtures for testing

import pytest
from app import app, db
from app.models import User, Post
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta

@pytest.fixture(scope='function')
def new_user():
    user = User(username='Rahul', email='rahul@mail.com',
            password_hash=generate_password_hash('password'))

    return user

@pytest.fixture(scope='function')
def add_new_user(new_user):
    '''
    In case of error the database can contain the test user.
    If so delete the user first.
    '''
    user_from_db = User.query.filter_by(username=new_user.username).first()
    if user_from_db is not None:
        db.session.delete(user_from_db)
        db.session.commit()

    db.session.add(new_user)
    db.session.commit()

    user_from_db = User.query.filter_by(username=new_user.username).first()
    yield user_from_db

    db.session.delete(user_from_db)
    db.session.commit()

@pytest.fixture(scope='function')
def new_post():
    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0)

    user = User(username='Rahul', email='rahul@mail.com',
            password_hash=generate_password_hash('password'))

    post = Post(timestamp=timestamp, body='Flask is awesome.', author=user)

    return user, post;

@pytest.fixture(scope='function')
def add_new_post(new_post):
    '''
    In case of error the database can contain the test user and post.
    If so delete the user and post first.
    '''
    user, post = new_post

    user_from_db = User.query.filter_by(username=user.username).first()
    if user_from_db is not None:
        post_from_db = Post.query.filter_by(author=user_from_db).first()
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
def test_client():
    return app.test_client()
