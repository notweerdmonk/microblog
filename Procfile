#web: flask run --host=0.0.0.0
#web: authbind gunicorn -w 4 -b 0.0.0.0:80 wsgi:app
web: flask db upgrade; gunicorn wsgi:app
worker: rq worker microblog-tasks
