from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, FileField, \
    SelectField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

required_message = 'Поле c {} обязательно для заполнения'
email_message = 'Недействительный адрес электронной почты'


class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм',
                           validators=[DataRequired(message=required_message.format('никнеймом'))])
    login = StringField('Логин',
                        validators=[DataRequired(message=required_message.format('логином'))])
    email = EmailField('Электронная почта',
                       validators=[
                           DataRequired(message=required_message.format('электронной почтой')),
                           Email(message=email_message)])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message=required_message.format('паролем'))])
    repeat_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired(
                                        message=required_message.format('повтором пароля'))])
    # recaptcha_field = RecaptchaField()
    submit = SubmitField('Регистрация')


class AuthorizationForm(FlaskForm):
    login = StringField('Логин',
                        validators=[DataRequired(message=required_message.format('логином'))])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message=required_message.format('паролем'))])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')
