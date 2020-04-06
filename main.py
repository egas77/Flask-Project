from flask import render_template, redirect, url_for, flash, abort, request, make_response, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from flask_restful import abort

import datetime
import requests
import base64

from app import app, login_manager, get_session, api
from app.forms import RegisterForm, AuthorizationForm, UserForm
from app.models import User
from app.token import send_confirm_message, confirm_token
from app.user_api import UserResource


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_query().get(user_id)


@app.route('/registration', methods=['GET', 'POST'])
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
                'redirect_url': url_for('index')
            }), 200)
        else:
            return make_response(jsonify(response.json()), response.status_code)
    elif request.method == 'POST' and not register_form.validate_on_submit():
        errors = {}
        for error in register_form.login.errors:
            errors['login'] = error
        for error in register_form.email.errors:
            errors['email'] = error
        for error in register_form.password.errors:
            errors['password'] = error
        for error in register_form.repeat_password.errors:
            errors['repeat_password'] = error
        if errors:
            return make_response(jsonify({'message': errors}), 400)
    elif request.method == 'GET':
        return render_template('registration.html', register_form=register_form, title=title)


@app.route('/confirm/<token>')
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
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
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
                    'redirect_url': url_for('index')
                }), 200)
            return make_response(jsonify({
                'message': {'Ошибка': 'Неверный пароль'}
            }), 400)
        return make_response(jsonify({
            'message': {'Ошибка': 'Пользователь с таким логином не найден'}
        }), 400)
    elif request.method == 'POST' and not authorization_form.validate_on_submit():
        errors = {}
        for error in authorization_form.login.errors:
            errors['login'] = error
        for error in authorization_form.password.errors:
            errors['password'] = error
        if errors:
            return make_response(jsonify({'message': errors}), 400)
    elif request.method == 'GET':
        return render_template('login.html', authorization_form=authorization_form, title=title)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_page(user_id):
    if user_id != int(current_user.get_id()) and current_user.importance != 2:
        flash('У вас нет прав доступа к этому аккаунту', 'error')
        return redirect(url_for('index'))
    user_form = UserForm()
    user = User.get_query().get(user_id)
    if user:
        if request.method == 'GET':
            return render_template('user.html', user_form=user_form, user=user)
    abort(401)


@app.route('/activate-email')
@login_required
def activate_email():
    result = send_confirm_message(current_user)
    if result['status']:
        return make_response(jsonify(
            {'message': result['message']}), 200)
    else:
        flash(result['message'], 'success')
        return redirect(url_for('index'))


@app.route('/subscribe')
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


@app.route('/user-image', methods=['POST'])
@login_required
def user_image():
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    flash(error, 'error')
    return render_template('index.html'), 404


@app.errorhandler(401)
def login_error(error):
    flash(error, 'error')
    return render_template('index.html'), 401


if __name__ == '__main__':
    app.run()
