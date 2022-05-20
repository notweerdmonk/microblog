from flask import render_template, flash, redirect, url_for, request, g
from app import db
from app.main.forms import EditProfileForm, NewPostForm, EmptyForm, SearchForm, \
        MessageForm
from app.models import User, Post, Message
from flask_login import login_required, current_user
from werkzeug.urls import url_parse
from datetime import datetime
from app.main import bp
from flask import current_app

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()

def new_post(user, form):
    post = Post(body=form.post_body.data, author=user)
    if post is not None:
        db.session.add(post)
        db.session.commit()

def pagination_urls(route, obj):
    return url_for(route, page=obj.prev_num) if obj.has_prev else None,\
        url_for(route, page=obj.next_num) if obj.has_next else None,

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NewPostForm()
    if form.validate_on_submit():
        new_post(current_user, form)
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts().paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    #prev_url, next_url = pagination_urls('main.index', posts)
    #return render_template('main/index.html', title = 'Home', posts=posts.items,
    #        prev_url=prev_url, next_url=next_url, forms=[form])
    return render_template('main/index.html', title = 'Home', posts=posts.items,
            pagination=posts, forms=[form])

@bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    form1 = NewPostForm()
    form2 = EmptyForm()
    if form1.validate_on_submit():
        new_post(current_user, form1)
        flash('Your post is now live!')
        return redirect(url_for('main.user', username=username))
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.post.order_by(Post.timestamp.desc())\
            .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    #prev_url = url_for('main.user', username=username, page=posts.prev_num) \
    #        if posts.has_prev else None
    #next_url = url_for('main.user', username=username, page=posts.next_num) \
    #        if posts.has_next else None
    #return render_template('main/user.html', user=user, posts=posts.items,
    #        prev_url=prev_url, next_url=next_url, forms=[form1, form2])
    return render_template('main/user.html', user=user, posts=posts.items,
            pagination=posts, forms=[form1, form2])

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit() and form.submit.data == True:
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    elif form.cancel.data == True:
        return redirect(url_for('main.user', username=current_user.username))
    return render_template('main/edit_profile.html', title='Edit Profile',
            form=form)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found!'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found!'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    #prev_url, next_url = pagination_urls('main.explore', posts)
    #return render_template('main/index.html', title='Explore', posts=posts.items,
    #        prev_url=prev_url, next_url=next_url)
    return render_template('main/index.html', title='Explore', posts=posts.items,
            pagination=posts)

class Paginator():
    def __init__(self, lst, page_number, per_page):
        n = len(lst)
        delta = n / per_page
        
        
@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts = Post.search(g.search_form.q.data, page,
            current_app.config['POSTS_PER_PAGE'])
    #next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
    #        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    #prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
    #        if page > 1 else None
    #return render_template('main/search.html', title='Search', posts=posts,
    #        next_url=next_url, prev_url=prev_url)
    return render_template('main/search.html', title='Search', posts = posts.items,
            pagination=posts)

@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter(User.username==recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('main.user', username=recipient))
    return render_template('main/send_message.html', title='Send message',
            form=form, recipient=recipient)

@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.received_messages.order_by(
            Message.timestamp.desc()).paginate(
                    page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('main/messages.html', messages=messages.items,
            pagination=messages)
