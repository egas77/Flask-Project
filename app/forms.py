from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email

required_message = 'Это поле обязательно для заполнения'
email_message = 'Недействительный адресс электронной почты'


class RegisterForm(FlaskForm):
    username = StringField('Имя',
                           validators=[DataRequired(message=required_message)])
    email = EmailField('Электронная почта',
                       validators=[DataRequired(message=required_message),
                                   Email(message=email_message)])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message=required_message)])
    repeat_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired(message=required_message)])
    submit = SubmitField('Регистрация')
