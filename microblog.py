from app import create_app, db
from app.models import User, Post, Notification, Message, Task

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Notification': Notification,
            'Message': Message, 'Task': Task}

if __name__ == '__main__':
    app.run()
