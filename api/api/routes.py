
import api

from api.annotations import api_wrapper, require_login, check_csrf
from api.common import WebSuccess, WebError, safe_fail

from flask import Blueprint, request, session

blueprint = Blueprint('api', __name__)

@blueprint.route('/status', methods=['GET'])
@api_wrapper
def status_hook():
    logged_in = api.user.is_logged_in()
    status = {
        'logged_in': logged_in,
    }
    if logged_in:
        scores = api.user.get_user_scores()
        status.update(scores)

    return WebSuccess(data=status)

@blueprint.route('/login', methods=['POST'])
@api_wrapper
def login():
    form = api.common.flat_multi(request.form)
    api.user.login(data=form)

    return WebSuccess('Logged in', {'next': api.question.get_next_question_url()})

@blueprint.route('/logout', methods=['GET'])
@api_wrapper
@require_login
def logout():
    api.user.logout()
    return WebSucces('Logged out')

@blueprint.route('/register', methods=['POST'])
@api_wrapper
def register():
    form = api.common.flat_multi(request.form)
    uid = api.user.create_user(data=form)

    session['uid'] = uid

    return WebSuccess('Registered as %s'%(form['username'],))

@blueprint.route('/question', methods=['POST'])
@api_wrapper
@check_csrf
@require_login
def question():

     return api.question.check_question(data=api.common.flat_multi(request.form))

