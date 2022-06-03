from app.api import bp
from flask import jsonify, request
from app.api.auth import token_auth
from app.models import User, Post
from flask import url_for, abort
from app import db
from app.api.errors import bad_request

@bp.route('/posts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_post(id):
    return jsonify(Post.query.get_or_404(id).to_dict())

@bp.route('/posts/<username>', methods=['GET'])
@token_auth.login_required
def get_posts(username):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    user_id = User.query.filter(User.username==username).first().id
    data = Post.to_collection_dict(Post.query.filter(Post.user_id==user_id),
        page, per_page, 'api.get_posts', username=username)
    return jsonify(data)

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    data = request.get_json() or {}
    if 'author' not in data or 'body' not in data:
        return bad_request('must include author and body fields')
    if token_auth.current_user().username != data['author']:
        abort(403)
    else:
        post = Post()
        post.from_dict(data)
        print(post)
        db.session.add(post)
        db.session.commit()
        response = jsonify(post.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_post', id=post.id)
        return response
