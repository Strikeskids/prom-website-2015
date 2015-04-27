
import api

from api.annotations import api_wrapper, require_login, check_csrf
from api.common import WebSuccess, WebError, safe_fail

from flask import Blueprint, request, session

blueprint = Blueprint('api', __name__)

@blueprint.route('/status')
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

@blueprint.route('/login')
@api_wrapper
@check_csrf
def login():
    api.user.login(**api.common.flat_multi(request.form))

    user = api.user.get_user()

    return WebSuccess('Logged in', {next: '/question%d'%(user['question'])})

@blueprint.route('/logout')
@api_wrapper
@require_login
def logout():
    api.user.logout()
    return WebSucces('Logged out')

@blueprint.route('/register')
@api_wrapper
@check_csrf
def register():
    uid = api.user.create_user(**api.common.flat_multi(request.form))

    session['uid'] = uid

    return WebSuccess('Registered as {}'%(request.form['username']))

@blueprint.route('/question')
@api_wrapper
@check_csrf
@require_login
def question():
     flat = api.common.flat_multi(request.form)
     num = flat['question']
     answer = flat['answer']

     return api.question.check_question(num, answer)
