import conftest
from werkzeug.security import check_password_hash
from datetime import datetime, timezone, timedelta

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, password_hash properties and 
    is_authenticated, is_active, is_anonymous and get_id methods.
    """
    assert new_user.username == 'Rahul'
    assert new_user.email == 'rahul@mail.com'
    assert check_password_hash(new_user.password_hash, 'password')
    assert new_user.is_authenticated == True
    assert new_user.is_active == True
    assert new_user.is_anonymous == False
    assert new_user.get_id() == str(new_user.id)

def test_new_post(new_post):
    """
    GIVEN a Post model
    WHEN a post is created
    THEN check the timestamp, body, user_id, author fields
    """
    (user, post) = new_post

    timestamp = datetime(year=2022, month=4, day=19,
            hour=15, minute=30, second=0, microsecond=0,
            tzinfo=timezone(timedelta(hours=5, minutes=30)))

    assert post.timestamp == timestamp
    assert post.body == 'Flask is awesome.'
    assert post.user_id == user.id
    assert post.author == user
