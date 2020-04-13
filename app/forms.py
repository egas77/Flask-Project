from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, StopValidation

required_message = 'Поле c {} обязательно для заполнения'
email_message = 'Недействительный адрес электронной почты'


class PasswordValidate(object):
    keyboard_rows = (
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "йцукенгшщзхъ",
        "фывапролджэё",
        "ячсмитьбю",
        "1234567890"
    )

    def __init__(self, min_len, max_len, message=None):
        self.message = message
        self.min_len = min_len
        self.max_len = max_len

    def __call__(self, form, field):
        password = field.data.strip()
        if self.min_len < len(password) < self.max_len:
            lower = False
            upper = False
            digit = False
            for symbol in password:
                if symbol.islower() and not lower:
                    lower = True
                elif symbol.isupper() and not upper:
                    upper = True
                elif symbol.isdigit() and not digit:
                    digit = True
                if lower and upper and digit:
                    break
            if not lower or not upper:
                raise StopValidation(
                    message='В пароле должны присутствоветь заглавные и строчные символы')
            if not digit:
                raise StopValidation(message='В пароле должны присутсвовать цифры')
            if lower and upper and digit:
                for count in range(len(password) - 2):
                    keyboard_error = any(map(
                        lambda keyboard_row: password[count: count + 3].lower() in keyboard_row,
                        PasswordValidate.keyboard_rows))
                    if keyboard_error:
                        raise StopValidation(
                            message='В пароле не должно быть 3 подряд идущих символов')
        else:
            raise StopValidation(
                message=f'Пароль должен быть от {self.min_len} до {self.max_len} символов')


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
                             validators=[DataRequired(message=required_message.format('паролем')),
                                         PasswordValidate(8, 32)])
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


class RecoveryPasswordFirst(FlaskForm):
    email = EmailField('Электронная почта',
                       validators=[
                           DataRequired(message=required_message.format('электронной почтой')),
                           Email(message=email_message)])
    submit = SubmitField('Восстановить')


class RecoveryPasswordLast(FlaskForm):
    password = PasswordField('Пароль',
                             validators=[DataRequired(message=required_message.format('паролем')),
                                         PasswordValidate(8, 32)])
    repeat_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired(
                                        message=required_message.format('повтором пароля'))])
    submit = SubmitField('Изменить')


class PasswordChange(FlaskForm):
    old_password = PasswordField('Старый пароль',
                                 validators=[
                                     DataRequired(
                                         message=required_message.format('старым паролем'))])
    password = PasswordField('Пароль',
                             validators=[DataRequired(message=required_message.format('паролем')),
                                         PasswordValidate(8, 32)])
    repeat_password = PasswordField('Повторите пароль',
                                    validators=[DataRequired(
                                        message=required_message.format('повтором пароля'))])
    submit = SubmitField('Изменить')
