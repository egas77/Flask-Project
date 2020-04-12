from flask import url_for, render_template, flash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from app import app, send_mail
import smtplib


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
    except SignatureExpired:
        flash('Срок дейсвия токена истек', 'error')
        return False
    except BadSignature:
        flash('Ошибка проверки подписи', 'error')
        return False
    except:
        flash('Непредвиденная ошибка проверки токена', 'error')
        return False
    return email


def send_confirm_message(user):
    if not user.confirmed:
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        subject = 'Пожалуйста подтвердите вашу почту'
        template = render_template('activate.html', confirm_url=confirm_url)
        confirm_message = Message(
            subject,
            recipients=[user.email],
            html=template,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )
        try:
            send_mail(confirm_message)
        except smtplib.SMTPAuthenticationError:
            return {
                'status': False,
                'message': 'Не удалось отправить сообщение'
            }

        return {
            'status': True,
            'message': 'На вашу почту отправлена инструкция для активации аккаунта'
        }
    else:
        return {
            'status': False,
            'message': 'Аккаунт уже подтвержден'
        }


def send_recovery_password(user):
    token = generate_confirmation_token(user.email)
    recovery_url = url_for('user.recovery_password_last', token=token, _external=True)
    subject = 'Восстановление пароля'
    template = render_template('recovery_password_message.html', recovery_url=recovery_url)
    confirm_message = Message(
        subject,
        recipients=[user.email],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    try:
        send_mail(confirm_message)
    except smtplib.SMTPAuthenticationError:
        return {
            'status': False,
            'message': 'Не удалось отправить сообщение'
        }
    return {
        'status': True,
        'message': 'На вашу почту отправлена инструкция для восстановления пароля'
    }
