import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def get_admin_emails(env_var_name):
    env_var = os.environ.get(env_var_name); 
    if env_var is not None:
        env_var = list(env_var.split(','))
    return env_var


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = get_admin_emails('ADMINS') or ['email@example.com']
 
    POSTS_PER_PAGE = 10

