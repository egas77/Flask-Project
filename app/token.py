from flask import url_for, render_template, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app import app, mail


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_confirm_message(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    subject = "Пожалуйста подтвердите вашу почту"
    template = render_template('activate.html', confirm_url=confirm_url)
    with app.app_context():
        confirm_message = Message(
            subject,
            recipients=[user.email],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(confirm_message)
    flash('На вашу почту отправлена инструкция для подтверждения регистрации', 'warning')
