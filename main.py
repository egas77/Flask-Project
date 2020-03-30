from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user

from app import app, login_manager, get_session
from app.forms import RegisterForm
from app.models import User


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
        user = User()
        user.username = register_form.username.data
        user.email = register_form.email.data
        user.set_password(register_form.password.data)
        session = get_session()
        session.add(user)
        session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', register_form=register_form, title=title)


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
