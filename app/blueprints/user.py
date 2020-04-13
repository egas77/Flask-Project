from flask import Blueprint, render_template, request, flash, make_response, jsonify, url_for, \
    redirect, abort
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc
from app import login_manager, api, get_session, app
from app.models import User, Post
from app.forms import RegisterForm, AuthorizationForm, RecoveryPasswordFirst, RecoveryPasswordLast, PasswordChange
from app.user_api import UserResource
from app.token import send_confirm_message, confirm_token, send_recovery_password

import requests
import base64
import datetime
import os

blueprint_user = Blueprint('user', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    return User.get_query().get(user_id)


@blueprint_user.route('/registration', methods=['GET', 'POST'])
def registration():
    register_form = RegisterForm()
    title = 'Регистрация'
    if register_form.validate_on_submit():
        response = requests.post(api.url_for(UserResource, _external=True),
                                 json=request.form.to_dict())
        if response:
            flash('Регистрация прошла успешно', 'success')
            user = User.get_query().get(response.json()['user_id'])
            login_user(user)
            result = send_confirm_message(user)
            if result['status']:
                flash(result['message'], 'warning')
            else:
                flash(result['message'], 'success')
            return make_response(jsonify({
                'redirect': True,
                'redirect_url': url_for('main.index')
            }), 200)
        else:
            return make_response(jsonify(response.json()), response.status_code)
    elif request.method == 'POST' and not register_form.validate_on_submit():
        return make_response(jsonify({'message': register_form.errors}), 400)
    elif request.method == 'GET':
        return render_template('registration.html', register_form=register_form, title=title)


@blueprint_user.route('/confirm/<token>')
@login_required
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        return redirect(url_for('index'))
    user = User.get_query().filter(User.email == email).first_or_404()
    if current_user.email != user.email:
        abort(401)
    if user.confirmed:
        flash('Аккаунт уже подтвержден', 'success')
    else:
        user.confirmed = True
        user.confirmed_date = datetime.datetime.now()
        session = get_session()
        session.commit()
        flash('Учетная запись успешно подтверждена', 'success')
    return redirect(url_for('main.index'))


@blueprint_user.route('/login', methods=['GET', 'POST'])
def login():
    authorization_form = AuthorizationForm()
    title = 'Авторизация'
    if authorization_form.validate_on_submit():
        login_data = authorization_form.login.data
        password = authorization_form.password.data
        remember = authorization_form.remember.data
        user = User.get_query().filter(User.login == login_data).first()
        if user:
            if user.check_password(password):
                login_user(user, remember=remember)
                return make_response(jsonify({
                    'redirect': True,
                    'redirect_url': url_for('main.index')
                }), 200)
            return make_response(jsonify({
                'message': {'Ошибка': 'Неверный пароль'}
            }), 400)
        return make_response(jsonify({
            'message': {'Ошибка': 'Пользователь с таким логином не найден'}
        }), 400)
    elif request.method == 'POST' and not authorization_form.validate_on_submit():
        return make_response(jsonify({'message': authorization_form.errors}), 400)
    elif request.method == 'GET':
        return render_template('login.html', authorization_form=authorization_form, title=title)


@blueprint_user.route('/user/<int:user_id>')
@blueprint_user.route('/user/<int:user_id>/<int:post_page>')
@login_required
def user_page(user_id, post_page=1):
    if user_id != int(current_user.get_id()) and current_user.importance not in [1, 2]:
        flash('У вас нет прав доступа к этому аккаунту', 'error')
        return redirect(url_for('index'))
    password_form = PasswordChange()
    user = User.get_query().get_or_404(user_id)
    if user.importance in [1, 2]:
        posts = user.posts.order_by(desc(Post.publication_date)
                                    ).paginate(post_page, app.config.get('USERS_ON_USER_PAGE', 10))
        return render_template('user.html', user=user, posts=posts, password_form=password_form)
    return render_template('user.html', user=user, password_form=password_form)


@blueprint_user.route('/activate-email')
@login_required
def activate_email():
    result = send_confirm_message(current_user)
    if result['status']:
        return make_response(jsonify(
            {'message': result['message']}), 200)
    else:
        return make_response(jsonify(
            {'message': result['message']}), 200)


@blueprint_user.route('/subscribe')
@login_required
def subscribe():
    user_id = current_user.get_id()
    if current_user.subscription:
        requests.put(api.url_for(UserResource, user_id=user_id, _external=True),
                     json={'subscription': False})
    else:
        requests.put(api.url_for(UserResource, user_id=user_id, _external=True),
                     json={'subscription': True})
    return make_response(jsonify({
        'subscribe_status': current_user.subscription
    }), 200)


@blueprint_user.route('/user-image', methods=['POST'])
@login_required
def user_image():
    current_image = current_user.image_file
    if current_image:
        os.remove(f'app/static/{current_image}')
    data_image = request.form.get('image').split(',', maxsplit=1)
    format_img = data_image[0].split('/')[1].split(';')[0]
    base_64_srt = data_image[1]
    file_content = base64.b64decode(base_64_srt)
    url_file = f'app/static/img/users_avatar/{current_user.get_id()}.{format_img}'
    with open(url_file, mode='wb') as img_file:
        img_file.write(file_content)
    filename = f'img/users_avatar/{current_user.get_id()}.{format_img}'
    user_id = current_user.get_id()
    response = requests.put(api.url_for(UserResource, user_id=user_id, _external=True),
                            json={'image_file': filename})
    if response:
        return make_response(jsonify({'status': 'ok'}), 200)
    else:
        return make_response(jsonify({'status': 'error server'}), 400)


@blueprint_user.route('/edit-user', methods=['POST'])
@login_required
def edit_user():
    old_password = request.form.get('old_password', None)
    if old_password:
        if not current_user.confirmed:
            return make_response(jsonify({
                'message': {'Ошибка': 'Аккаунт не подтвержден'}
            }), 400)
        password_form = PasswordChange()
        if not password_form.validate_on_submit():
            return make_response(jsonify({
                'message': password_form.errors
            }), 400)
        if not current_user.check_password(old_password):
            return make_response(jsonify({
                'message': {'Ошибка': 'Неверный пароль'}
            }), 400)
    user_id = current_user.get_id()
    response = requests.put(api.url_for(UserResource, user_id=user_id, _external=True),
                            json=request.form.to_dict())
    if response:
        return make_response(jsonify({'message': 'status ok'}), 200)
    else:
        return make_response(jsonify(response.json()), 400)


@blueprint_user.route('/edit-importance', methods=['POST'])
def edit_importance():
    user_id = request.form.get('user_id')
    user = User.get_query().get(user_id)
    if not user:
        return make_response(jsonify({
            'message': 'Пользователь не найден'
        }), 200)
    response = requests.put(api.url_for(UserResource, user_id=user_id, _external=True),
                            json=request.form.to_dict())
    if response:
        return make_response(jsonify({'message': 'status ok'}), 200)
    else:
        return make_response(jsonify(response.json()), 400)


@blueprint_user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@blueprint_user.route('/recovery-password-first', methods=['GET', 'POST'])
def recovery_password_first():
    recovery_form = RecoveryPasswordFirst()
    if recovery_form.validate_on_submit():
        email = request.form.get('email')
        user = User.get_query().filter(User.email == email).first()
        if not user:
            return make_response(jsonify({
                'message': {'Ошибка': 'Пользователь с такой почтой не зарегистрирован'}
            }), 400)
        result = send_recovery_password(user)
        flash(result['message'], 'success')
        return make_response(jsonify({
            'redirect': True,
            'redirect_url': url_for('main.index')
        }), 200)
    return render_template('recovery_password_first.html', recovery_form=recovery_form,
                           title='Восстановить пароль')


@blueprint_user.route('/recovery-password-last/<token>', methods=['GET', 'POST'])
def recovery_password_last(token):
    email = confirm_token(token)
    if not email:
        return redirect(url_for('index'))
    user = User.get_query().filter(User.email == email).first()
    recovery_form = RecoveryPasswordLast()
    if recovery_form.validate_on_submit():
        response = requests.put(api.url_for(UserResource, user_id=user.id, _external=True),
                                json=request.form.to_dict())
        if response:
            flash('Ваш пароль успешно изменен', 'success')
            return make_response(jsonify({
                'redirect': True,
                'redirect_url': url_for('main.index')
            }), 200)
        else:
            return make_response(jsonify(response.json()), 400)
    return render_template('recovery_password_last.html', recovery_form=recovery_form,
                           title='Новый пароль', token=token)


@blueprint_user.route('/list_user')
@blueprint_user.route('/list_user/<int:page>')
@login_required
def list_user(page=1):
    if current_user.importance != 2:
        abort(401)
    users = User.get_query().paginate(page, app.config.get('USERS_ON_PAGE', 10))
    return render_template('list_users.html', users=users)
