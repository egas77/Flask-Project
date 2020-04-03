from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from app import get_session
from app.models import User


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('login', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)
    parser.add_argument('repeat_password', required=True)

    def get(self, user_id):
        user = User.get_query().get(user_id)
        if not user:
            abort(400, message='User not found')
        return jsonify(
            user.to_dict()
        )

    def post(self):
        args = UserResource.parser.parse_args()  # <class 'requests.models.Response'>
        if args['password'] != args['repeat_password']:
            abort(400, message={'Ошибка': 'Пароли не совпадают'})
        repeat_user_login = User.get_query().filter(User.login == args['login']).first()
        if repeat_user_login:
            abort(400, message={'Ошибка': 'Пользователь с таким логином уже зарегистрирован'})
        repeat_user_email = User.get_query().filter(
            User.email == args['email']).first()
        if repeat_user_email:
            abort(400, message={'Ошибка': 'Пользователь с такми email уже зарегистрирован'})
        user = User()
        user.login = args['login']
        user.email = args['email']
        user.set_password(args['password'])
        user.confirmed = False
        session = get_session()
        session.add(user)
        # session.commit()
        return make_response(
            jsonify({'redirect': False}), 200
        )


class Users(Resource):
    def get(self):
        pass
