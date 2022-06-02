import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_bootstrap import Bootstrap5
from elasticsearch import Elasticsearch
from redis import Redis
import rq

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()
moment = Moment()
bootstrap = Bootstrap5()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    elasticsearch_url = app.config['ELASTICSEARCH_URL']
    elasticseach_cert = app.config['ELASTICSEARCH_CERT']
    elasticseach_username = app.config['ELASTICSEARCH_USERNAME']
    elasticsearch_password = app.config['ELASTICSEARCH_PASSWORD']
    app.elasticsearch = Elasticsearch(
            elasticsearch_url,
            ca_certs=elasticseach_cert,
            basic_auth=(elasticseach_username, elasticsearch_password)) \
        if elasticsearch_url else None

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                    fromaddr='no_reply@' + app.config['MAIL_SERVER'],
                    toaddrs=app.config['ADMINS'],
                    subject='Microblog Failure',
                    credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler=RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                backupCount=5)
        file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Starting up Microblog server')

    return app

from app import models
