![Tests](https://github.com/notweerdmonk/microblog/actions/workflows/python-app.yml/badge.svg?branch=development)

# Flask tutorial with micro-blogging application.

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Deployed: https://anothermicroblog.herokuapp.com
- Exporting posts will not work
- Full text search works with Postgresql
- Site may not be up because of free dyno limitation

## Additional features:

### Bootstrap 5

Uses bootstrap-flask which supports Bootstrap 5.

### APIs related to blog posts

| HTTP Method | URL                         | Notes                                   |
|-------------|-----------------------------|-----------------------------------------|
| GET         | /api/posts/&lt;id&gt;       | Return a post.                          |
| GET         | /api/posts/&lt;username&gt; | Return the collection of posts by user. |
| POST        | /api/posts                  | Create a new post for user.             |

### Application testing with pytest

#### Unit tests
- Test user and post model creation
- Test user and post addition to database
- Test follow and unfollow actions

#### Funtional tests
- Test response of routes for anonymous user
- Test response of routes for authenticated user
- Test response of routes for authorization token
