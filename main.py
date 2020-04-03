from flask import render_template, redirect, url_for, flash, abort, request, make_response, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from flask_restful import abort

import datetime
import requests

from app import app, login_manager, get_session, api, socket
from app.forms import RegisterForm, AuthorizationForm
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
                                 data=request.form.to_dict())
        if response:
            flash('Регистрация прошла успешно', 'success')
            return make_response(jsonify({
                'redirect': True,
                'redirect_url': url_for('index')
            }), 200)
        else:
            return make_response(jsonify(response.json()), response.status_code)
    elif request.method == 'POST':
        error = False
        for error in register_form.login.errors:
            socket.emit('registration_validate_error', error)
            error = True
        for error in register_form.email.errors:
            socket.emit('registration_validate_error', error)
            error = True
        for error in register_form.password.errors:
            socket.emit('registration_validate_error', error)
            error = True
        for error in register_form.repeat_password.errors:
            socket.emit('registration_validate_error', error)
            error = True
        if error:
            return make_response(jsonify({
                'redirect': False
            }), 400)
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
        user.confirmed_on = datetime.datetime.now()
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
                return redirect(url_for('index'))
            else:
                flash('Неверный пароль', 'error')
        else:
            flash('Пользователь с таким логином не найден', 'error')
    else:
        for error in authorization_form.login.errors:
            flash(error, 'error')
        for error in authorization_form.password.errors:
            flash(error, 'error')
    return render_template('login.html', authorization_form=authorization_form, title=title)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    flash(error, 'danger')
    return render_template('index.html'), 404


@app.errorhandler(401)
def login_error(error):
    flash(error, 'danger')
    return render_template('index.html'), 401


if __name__ == '__main__':
    app.run()
