from flask import Blueprint, render_template, request, make_response, jsonify, redirect, url_for, \
    flash
from flask_login import login_required, current_user
from flask_mail import Message
from sqlalchemy import desc

from app import app, api, send_mail, get_session
from app.models import Post, User, Comment
from app.post_api import PostResource

import requests
import datetime

from threading import Thread

blueprint_post = Blueprint('post', __name__, template_folder='templates')


@blueprint_post.route('/create-post', methods=['GET', 'POST'])
@blueprint_post.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def create_post(post_id=None):
    if current_user.importance == 0:
        flash('У вас нет доступа к данной странице', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        json = request.form.to_dict()
        if post_id:
            response = requests.put(api.url_for(PostResource, post_id=post_id, _external=True),
                                    json=json)
        else:
            json['author_id'] = current_user.get_id()
            response = requests.post(api.url_for(PostResource, _external=True), json=json)
            subscribe_new_post(response.json()['post_id'])
        if response:
            return redirect(url_for('index'))
        else:
            return make_response(jsonify(response.json()), 400)
    if post_id:
        post = Post.get_query().get(post_id)
        if current_user.importance == 2 or post.author.get_id() == current_user.get_id():
            return render_template('new_post.html', post=post)
        else:
            flash('Вы не можете редактировать этот пост', 'error')
            return redirect(url_for('index'))
    return render_template('new_post.html')


@blueprint_post.route('/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    if current_user.importance == 0:
        return make_response(jsonify({
            'message': {'Ошибка': 'У вас нет прав не это действие'}
        }), 400)
    post = Post.get_query().get_or_404(post_id)
    if current_user.importance == 2 or post.author.get_id() == current_user.get_id():
        response = requests.delete(api.url_for(PostResource, post_id=post_id, _external=True))
        if not response:
            flash(response.json()['message'], 'error')
            return make_response(jsonify(response.json()), response.status_code)
        return make_response(jsonify({
            'status': 'OK'
        }), 200)
    else:
        return make_response(jsonify({
            'message': {'Ошибка': 'У вас нет прав не это действие'}
        }), 401)


@blueprint_post.route('/post/<int:post_id>')
@blueprint_post.route('/post/<int:post_id>/<int:comment_page>')
def view_post(post_id, comment_page=1):
    post = Post.get_query().get_or_404(post_id)
    comments = Comment.get_query().filter(Comment.post_id == post_id).order_by(
        desc(Comment.publication_date)).paginate(comment_page,
                                                 app.config.get('COMMENTS_ON_PAGE', 10), False)
    return render_template('post.html', post=post, comments=comments)


@blueprint_post.route('/create_comment', methods=['POST'])
def create_comment():
    user_id = request.form.get('user_id')
    post_id = request.form.get('post_id')
    content = request.form.get('content')
    comment = Comment(author_id=user_id, post_id=post_id, content=content)
    comment.publication_date = datetime.datetime.now()
    comment.publication_date_string = comment.publication_date.strftime('%d.%m.%Y %H:%M')
    session = get_session()
    session.add(comment)
    session.commit()
    return make_response(jsonify({
        'status': 'OK',
    }), 200)


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
    if not users:
        return
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
