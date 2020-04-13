from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from app import get_session
from app.models import User
import datetime


class UserResource(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('nickname', required=True)
    parser_post.add_argument('login', required=True)
    parser_post.add_argument('email', required=True)
    parser_post.add_argument('password', required=True)
    parser_post.add_argument('repeat_password', required=True)

    parser_put = reqparse.RequestParser()
    parser_put.add_argument('email')
    parser_put.add_argument('password')
    parser_put.add_argument('repeat_password')
    parser_put.add_argument('nickname')
    parser_put.add_argument('importance', type=int)
    parser_put.add_argument('confirmed', type=bool)
    parser_put.add_argument('subscription', type=bool)
    parser_put.add_argument('image_file')

    def get(self, user_id):
        user = User.get_query().get(user_id)
        if not user:
            abort(400, message={'Error': 'User not found'})
        return make_response(jsonify(
            user.to_dict()
        ), 200)

    def post(self):
        args = UserResource.parser_post.parse_args()  # <class 'requests.models.Response'>
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
        user.nickname = args['nickname']
        user.login = args['login']
        user.email = args['email']
        user.create_date = datetime.datetime.now()
        user.set_password(args['password'])
        user.confirmed = False
        session = get_session()
        session.add(user)
        session.commit()
        return make_response(
            jsonify(
                {
                    'redirect': False,
                    'user_id': user.id
                }
            ), 200
        )

    def put(self, user_id):
        args = UserResource.parser_put.parse_args()
        user = User.get_query().get(user_id)
        if args['password'] is not None:
            if args['password'] != args['repeat_password']:
                abort(400, message={'Ошибка': 'Пароли не совпадают'})
        if args['email'] is not None:
            duplicate_email_user = User.get_query().filter(User.email == args['email']).first()
            if duplicate_email_user:
                abort(400, message={'Ошибка': 'Пользователь с такми email уже зарегистрирован'})
            else:
                user.confirmed = False
                user.subscription = False
        for key, value in args.items():
            if value is not None:
                if key == 'password':
                    user.set_password(value)
                else:
                    user.__setattr__(key, value)
        get_session().commit()
        return make_response(jsonify({
            'status': 'OK'
        }), 200)

    def delete(self, user_id):
        user = User.get_query().get(user_id)
        if not user:
            abort(400, message={'Error': 'User not found'})
        else:
            session = get_session()
            session.delete(user)
            session.commit()
            return make_response(jsonify({
                'status': 'OK'
            }), 200)
