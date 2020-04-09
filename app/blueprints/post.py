from flask import Blueprint, render_template, request, make_response, jsonify, redirect, url_for
from flask_login import login_required
from flask_mail import Message

from app import app, api, send_mail
from app.models import Post, User
from app.post_api import PostResource

import requests

from threading import Thread

blueprint_post = Blueprint('post', __name__, template_folder='templates')


@blueprint_post.route('/create-post', methods=['GET', 'POST'])
@blueprint_post.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def create_post(post_id=None):
    if request.method == 'POST':
        if post_id:
            response = requests.put(api.url_for(PostResource, post_id=post_id, _external=True),
                                    json=request.form.to_dict())
        else:
            response = requests.post(api.url_for(PostResource, _external=True),
                                     json=request.form.to_dict())
            subscribe_new_post(response.json()['post_id'])
        if response:
            return redirect(url_for('index'))
        else:
            return make_response(jsonify(response.json()), 400)
    if post_id:
        post = Post.get_query().get(post_id)
        return render_template('new_post.html', post=post)
    return render_template('new_post.html')


@blueprint_post.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.get_query().get(post_id)
    return render_template('post.html', post=post)


@blueprint_post.route('/upload-image', methods=['POST'])
@login_required
def upload_image_creator():
    image = request.files.get('upload')
    url_image = '/static/img/' + image.filename
    image.save('app/' + url_image)
    return make_response(jsonify({
        'uploaded': 1,
        'fileName': image.filename,
        'url': url_image
    }))


def subscribe_new_post(post_id):
    users = User.get_query().filter(User.subscription).all()
    subject = 'Вышла новая запись'
    url = url_for('post.view_post', post_id=post_id, _external=True)
    template = render_template('new_post_subscribe.html', url=url)
    message = Message(
        subject,
        recipients=list(map(lambda user: user.email, users)),
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    thr = Thread(target=send_mail, args=[message])
    thr.start()
    return thr
