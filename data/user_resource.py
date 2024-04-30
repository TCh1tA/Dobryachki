from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from . import db_session
from .user import User
from .user_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def set_password(password):
    return generate_password_hash(password)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        return jsonify({
            'user': user.to_dict(only=('name', 'surname', 'age'))
        })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.delete(user)
        sess.commit()
        sess.close()
        return jsonify({'delete success': f'user_id {user_id}'})


class UserResourceList(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({
            'users': [item.to_dict(only=('name', 'surname', 'position', 'age')) for item in users]
        })

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_passwors=set_password(args['hashed_password'])
        )
        sess.add(user)
        sess.commit()
        sess.close()
        return jsonify({'success': 'OK'})