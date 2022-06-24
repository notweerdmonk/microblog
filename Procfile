web: flask db upgrade; gunicorn wsgi:app
worker: rq worker -u $REDIS_URL microblog-tasks
