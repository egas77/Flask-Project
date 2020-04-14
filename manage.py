from app import manager, get_session
from app.models import User, Post, Comment

from flask_migrate import MigrateCommand
import requests

manager.add_command('db', MigrateCommand)


@manager.command
def create_admin():
    """Command for create admin"""
    print('Введите никнейм:')
    nickname = input()
    print('Введите логин:')
    login = input()
    print('Введите адрес электронной почты:')
    email = input()
    print('Ведите пароль:')
    password = input()
    print('Повторите пароль:')
    repeat_password = input()
    response = requests.post('http://127.0.0.1:5000/user-api',
                             data={
                                 'nickname': nickname,
                                 'login': login,
                                 'email': email,
                                 'password': password,
                                 'repeat_password': repeat_password,
                             })
    if response:
        user_id = response.json()['user_id']
        user = User.get_query().get(user_id)
        user.importance = 2
        get_session().commit()
        print('Create admin success')
        print(f'Id for {user}: {user_id}')
        print('Потвердите ваш аккаунт в личном кабинете')
    else:
        print(response.json())


@manager.command
def clear_users():
    """Delete all users"""
    users = get_session().query(User).all()
    if users:
        for user in users:
            delete_id(user.id)
    else:
        print('Users not found')


@manager.command
def delete_login(login):
    """Delete user on login"""
    user = User.get_query().filter(User.login == login).first()
    if user:
        delete_id(user.id)
    else:
        print('User not found')


@manager.command
def delete_id(user_id):
    """Delete user on id"""
    user = User.get_query().get(user_id)
    if user:
        response = requests.delete('http://127.0.0.1:5000/user-api/{}'.format(user.id))
        if not response:
            print(response)
        else:
            print(user, 'deleted')
    else:
        print('User not found')


@manager.command
def list_users():
    """List users"""
    users = User.get_query().all()
    for user in users:
        print(user)
    if not users:
        print('Users not found')


@manager.command
def clear_data_base():
    """Clear all data in data base"""
    session = get_session()
    comments = Comment.get_query().all()
    for comment in comments:
        session.delete(comment)
    posts = Post.get_query().all()
    for post in posts:
        session.delete(post)
    users = User.get_query().all()
    for user in users:
        session.delete(user)
    session.commit()


if __name__ == '__main__':
    manager.run()
