from flask import Blueprint, jsonify, abort

from app.models import User

blueprint = Blueprint('user', __name__, template_folder='templates')


@blueprint.route('/get_users', methods=['GET'])
def get_users():
    users = User.get_query().all()
    if not users:
        return jsonify({
            'error': 'Users not found'
        })
    if users:
        return jsonify({
            'users': [user.to_dict(only=('id', 'login', 'username')) for user in users]
        })


@blueprint.route('/get_user/<int:user_id>')
def get_user(user_id):
    user = User.get_query().get(user_id)
    if not user:
        return abort(404)
    return jsonify({
        'user': user.to_dict()
    })
