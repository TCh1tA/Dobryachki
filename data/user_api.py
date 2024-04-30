import flask

from . import db_session
from . import user
from .user import User

blueprint = flask.Blueprint(
    'get_user',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_user():
    d = {}
    sess = db_session.create_session()
    req = sess.query(User).all()
    for el in req:
        d[el.id] = {
            'id': el.id,
            'name': el.name,
            'email': el.email,
            'hashed_password': el.hashed_password,
            'p_time': el.p_time,
            'custom_podd': el.custom_podd,
            'prem_image': el.prem_image
        }
    return flask.jsonify(d)