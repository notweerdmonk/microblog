from flask import render_template, flash, redirect, url_for
from flask import get_flashed_messages, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, NewPostForm, EmptyForm
from app.models import User, Post
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def new_post(user, form):
    post = Post(body=form.post_body.data, author=user)
    if post is not None:
        db.session.add(post)
        db.session.commit()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NewPostForm()
    if form.validate_on_submit():
        new_post(current_user, form)
        return redirect(url_for('index'))
    posts = current_user.posts().all()
    return render_template('index.html', title = 'Home', posts=posts, forms=[form])

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
            flash('Invalid username or password')
            return redirect(url_for('login'))
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

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form1 = NewPostForm()
    form2 = EmptyForm()
    if form1.validate_on_submit():
        new_post(current_user, form1)
        return redirect(url_for('user', username=username))
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template(
            'user.html', user=user, posts=posts, forms=[form1, form2])

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit() and form.submit.data == True:
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    elif form.cancel.data == True:
        return redirect(url_for('user', username=current_user.username))
    return render_template('edit_profile.html', title='Edit Profile',
            form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found!'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found!'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are following {}'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
    
