from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message

import datetime

from app import app, mail, login_manager, get_session
from app.forms import RegisterForm
from app.models import User
from app.token import generate_confirmation_token, confirm_token


@app.route('/')
@app.route('/index')
def index():
    flash('Error')
    flash('Error2')
    flash('56635253536466645656')
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get_query().get(user_id)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    register_form = RegisterForm()
    title = 'Регистрация'
    if register_form.validate_on_submit():
        user = User()
        user.username = register_form.username.data
        user.email = register_form.email.data
        user.set_password(register_form.password.data)
        user.confirmed = False
        session = get_session()
        session.add(user)
        session.commit()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        template = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        with app.app_context():
            confirm_message = Message(
                subject,
                recipients=[user.email],
                html=template,
                sender=app.config['MAIL_DEFAULT_SENDER']
            )
            mail.send(confirm_message)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('registration.html', register_form=register_form, title=title)


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.get_query().filter_by(email=email).first_or_404()
    if current_user.email != user.email:
        abort(404)
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        session = get_session()
        session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
