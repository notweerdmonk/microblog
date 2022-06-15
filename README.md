# Flask tutorial with micro-blogging application.

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Additional features:

### Bootstrap 5

Uses bootstrap-flask which supports Bootstrap 5.

### APIs related to blog posts

| HTTP Method | URL                   | Notes                                   |
|-------------|-----------------------|-----------------------------------------|
| GET         | /api/posts/<id>       | Return a post.                          |
| GET         | /api/posts/<username> | Return the collection of posts by user. |
| POST        | /api/posts            | Create a new post for user.             |

### Application testing with pytest

#### Unit tests
- Test user and post model creation
- Test user and post addition to database
- Test follow and unfollow actions

#### Funtional tests
- Test response of routes for anonymous user
- Test response of routes for authenticated user
- Test response of routes for authorization token
