from flask import render_template, flash, redirect, url_for, get_flashed_messages, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Hari'},
            'body': 'Carrots are red!'
        },
        {
            'author': {'username': 'Ravi'},
            'body': 'To be or not to be.'
        }
    ]
    return render_template('index.html', title = 'Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        print(form.username)
        print(form.password)
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            print('Invalid username or password')
            flash('Invalid username or password')
            redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
        user = User(username=form.username.data, email=form.email.data)
        print(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, You are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)
