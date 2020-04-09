from flask import make_response, jsonify
from flask_restful import Resource, reqparse, abort
from app import get_session
from app.models import Post

import datetime


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
        session = get_session()
        session.add(post)
        session.commit()
        return make_response(jsonify({
            'status': 'OK'
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
