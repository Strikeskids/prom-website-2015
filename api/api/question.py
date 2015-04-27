
import api

from flask import request, session
from api.common import safe_fail, get_conn, WebSuccess, InternalException
from api.annotations import require_login

def has_solved(qid, uid=None):
    if not uid:
        if 'uid' not in session:
            raise InternalException('Need uid to see if solved')
        uid = session['uid']

    with get_conn() as cursor:
        query = 'SELECT 1 FROM `submissions` WHERE `correct` = 1 AND `qid` = %s AND `uid` = %s LIMIT 1;'

        cursor.execute(query, (qid, uid))

        return bool(len(cursor.fetchall()))

@require_login
def get_next_question_url(num=None, uid=None):
    if not num:
        if not uid:
            if 'uid' not in session:
                raise InternalException('Need uid to see next')
            uid = session['uid']
        scores = api.user.get_user_scores()
        num = scores['num'] or 0

    next_question = safe_fail(get_question, num=int(num)+1)

    if not next_question:
        url = '/survived'
    else:
        url = 'question%d'%(next_question['num'], )

    return url

@require_login
def check_question(num, answer):
    question = safe_fail(get_question, num=num)

    if not question:
        raise InternalException('Question not found')

    correct = question['answer'] in answer
    solved = safe_fail(has_solved, question['qid'])

    with get_conn() as cursor:
        uid = session['uid']

        points = question['success'] if correct else -question['failure']

        query = 'INSERT INTO `submissions` (`uid`, `qid`, `answer`, `points`, `correct`) VALUES (%s, %s, %s, %s, %s);'
        args = (uid, question['qid'], answer, points if not solved else 0, 1 if correct else 0)

        cursor.execute(query, args)

        if correct:
            return WebSuccess('Correct!', data={'url': get_next_question_url()})
        else:
            return WebError('Incorrect')

def add_question(num, name, answer, success, failure):
    with get_conn() as cursor:
        query = 'INSERT INTO `questions` (`qid`, `num`, `name`, `answer`, `success`, `failure`) VALUES (%s, %s, %s, %s, %s, %s);'

        qid = api.common.token()

        cursor.execute(query, (qid, num, name, answer, success, failure))

        return qid

def get_question(num=None, name=None, qid=None):
    with get_conn() as cursor:
        query = 'SELECT * FROM `questions` WHERE '

        wheres = []
        if num:
            wheres.append(('`num` = %s', num))
        if name:
            wheres.append(('`name` = %s', name))
        if qid:
            wheres.append(('`qid` = %s', qid))

        if not wheres:
            raise InternalException('Need a criterion for a question query')

        clauses, args = zip(*wheres)

        query += ' AND '.join(clauses) + ';'

        cursor.execute(query, tuple(args))

        return cursor.fetchone()
