import conftest
from werkzeug.security import check_password_hash
from datetime import datetime, timezone, timedelta
from app import db

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check username, email, password_hash properties are valid and
    is_authenticated id is True, is_active is False, is_anonymous is False
    and get_id method returns user id
    """
    assert new_user.username == 'Rahul'
    assert new_user.email == 'rahul@mail.com'
    assert check_password_hash(new_user.password_hash, 'password')
    assert new_user.is_authenticated == True
    assert new_user.is_active == True
    assert new_user.is_anonymous == False
    assert new_user.get_id() == str(new_user.id)

def test_add_new_user(add_new_user):
    '''
    GIVEN an instance of User model
    WHEN the instance is added to database
    THEN check if database is updated correctly
    '''
    assert add_new_user.username == 'Rahul'
    assert add_new_user.email == 'rahul@mail.com'
    assert check_password_hash(add_new_user.password_hash, 'password')

def test_new_post(new_post):
    """
    GIVEN a Post model
    WHEN a post is created
    THEN check timestamp, body, user_id, author fields are valid
    """
    (user, post) = new_post

    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0)

    assert post.timestamp == timestamp
    assert post.body == 'Flask is awesome.'
    assert post.user_id == user.id
    assert post.author == user

def test_add_new_post(add_new_post):
    """
    GIVEN a Post model
    WHEN a post is created
    THEN check timestamp, body, user_id, author fields are valid
    """
    (user, post) = add_new_post

    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0)

    assert post.timestamp == timestamp
    assert post.body == 'Flask is awesome.'
    assert post.user_id == user.id
    assert post.author == user
