from flask import Blueprint, render_template, request, make_response, jsonify, redirect, url_for
from flask_login import login_required

from app import get_session
from app.models import Post

import datetime

blueprint_post = Blueprint('post', __name__, template_folder='templates')


@blueprint_post.route('/create-post', methods=['GET', 'POST'])
@blueprint_post.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def create_post(post_id=None):
    if request.method == 'POST':
        if post_id:
            post = Post.get_query().get(post_id)
        else:
            post = Post()
            post.publication_date = datetime.datetime.now()
        title = request.form.get('title-post')
        content = request.form.get('content', None)
        post.title = title
        post.content = content
        session = get_session()
        if not post_id:
            session.add(post)
        session.commit()
        return redirect(url_for('index'))
    if post_id:
        post = Post.get_query().get(post_id)
        return render_template('new_post.html', post=post)
    return render_template('new_post.html')


@blueprint_post.route('/post/<int:post_id>')
def view_post(post_id):
    print(post_id)
    post = Post.get_query().get(post_id)
    return render_template('post.html', post=post)


@blueprint_post.route('/upload-image', methods=['POST'])
@login_required
def upload_image_creator():
    image = request.files.get('upload')
    url_image = 'static/img/' + image.filename
    image.save('app/' + url_image)
    print(request.files)
    return make_response(jsonify({
        'uploaded': 1,
        'fileName': image.filename,
        'url': url_image
    }))
