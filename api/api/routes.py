
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
    flat = api.common.flat_multi(request.form)
    api.user.login(flat['username'], flat['password'])

    user = api.user.get_user()

    return WebSuccess('Logged in', {next: '/question%d'%(user['question'], )})

@blueprint.route('/logout', methods=['GET'])
@api_wrapper
@require_login
def logout():
    api.user.logout()
    return WebSucces('Logged out')

@blueprint.route('/register', methods=['POST'])
@api_wrapper
def register():
    flat = api.common.flat_multi(request.form)
    uid = api.user.create_user(flat['username'], flat['password'])

    session['uid'] = uid

    return WebSuccess('Registered as %s'%(flat['username'],))

@blueprint.route('/question', methods=['POST'])
@api_wrapper
@check_csrf
@require_login
def question():
     flat = api.common.flat_multi(request.form)
     num = flat['question']
     answer = flat['answer']

     return api.question.check_question(num, answer)

