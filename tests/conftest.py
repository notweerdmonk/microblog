# define fixtures for testing

import pytest
from app import app
from app.models import User, Post
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone, timedelta

@pytest.fixture(scope='function')
def new_user():
    user = User(username='Rahul', email='rahul@mail.com',
            password_hash=generate_password_hash('password'))

    return user

@pytest.fixture(scope='function')
def new_post():
    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0,
            tzinfo=timezone(timedelta(hours=5, minutes=30)))

    user = User(username='Rahul', email='rahul@mail.com',
            password_hash=generate_password_hash('password'))

    post = Post(timestamp=timestamp, body='Flask is awesome.', author=user)

    return user, post;

@pytest.fixture(scope='module')
def test_client():
    return app.test_client()
