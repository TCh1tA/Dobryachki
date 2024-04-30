import flask

from . import db_session
from . import jobs
from .jobs import Jobs

blueprint = flask.Blueprint(
    'get_jopan',
    __name__,
    template_folder='templates'
)


@blueprint.route('/test/jobs/<int:job_id>')
def get_jopan(job_id):
    d = {}
    sess = db_session.create_session()
    req = sess.query(Jobs).get(job_id)
    if not req:
        return flask.jsonify({'error': 'no'})
    else:
        return flask.jsonify({
            'jobs': [
                req.to_dict(only=('id', 'team_leader', 'job'))
            ]
        })
    # for el in req:
    #     d[el.id] = {
    #         'team_leader': el.team_leader,
    #         'job': el.job,
    #         'work_size': el.work_size,
    #         'collaborators': el.collaborators,
    #         'start_date': el.start_date,
    #         'end_date': el.end_date,
    #         'is_finished': el.is_finished
    #     }