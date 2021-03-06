from app.email import send_email
from flask import render_template
from flask import current_app

def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email('[Microblog] Reset Your Password',
            sender='no_reply@' + current_app.config['MAIL_SERVER'],
            recipients=[user.email],
            text_body=render_template('email/reset_password.txt',
                user=user, token=token),
            html_body=render_template('email/reset_password.html',
                user=user, token=token))
