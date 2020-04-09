from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from app import get_session
from app.models import Post

import datetime
import locale
import pymorphy2

locale.setlocale(locale.LC_ALL, 'ru')


def get_date_string():
    date = datetime.datetime.strftime(datetime.datetime.now(), '%d %B %H:%M').split()
    date[0] = str(int(date[0]))
    morph = pymorphy2.MorphAnalyzer()
    mount = morph.parse(date[1])[0].inflect({'gent'}).word
    date[1] = mount
    date_string = f'{date[0]} {date[1]}, {date[2]}'
    return date_string


class PostResource(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('title', required=True)
    parser_post.add_argument('content', required=True)

    parser_put = reqparse.RequestParser()
    parser_put.add_argument('title', required=True)
    parser_put.add_argument('content', required=True)

    def post(self):
        args = PostResource.parser_post.parse_args()
        post = Post()
        for key, item in args.items():
            post.__setattr__(key, item)
        post.publication_date = datetime.datetime.now()
        post.publication_date_string = get_date_string()
        session = get_session()
        session.add(post)
        session.commit()
        return make_response(jsonify({
            'status': 'OK',
            'post_id': post.id
        }), 200)

    def put(self, post_id):
        args = PostResource.parser_put.parse_args()
        post = Post.get_query().get(post_id)
        if not post:
            abort(400, message={'Ошибка': 'Пост не найден'})
        for key, value in args.items():
            post.__setattr__(key, value)
        session = get_session()
        session.commit()
        return make_response(jsonify({
            'status': 'OK'
        }), 200)

    def delete(self, post_id):
        post = Post.get_query().get(post_id)
        if not post:
            abort(400, message={'Ошибка': 'Пост не найден'})
        session = get_session()
        session.delete(post)
        session.commit()
        return make_response(jsonify({
            'status': 'OK'
        }), 200)
