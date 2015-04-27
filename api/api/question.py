
import api

from Flask import request, session

from api.common import safe_fail, get_conn, WebSuccess, InternalException

@require_login
def check_question(num, answer):
    question = safe_fail(get_question, num=num)

    if not question:
        raise InternalException('Question not found')

    correct = question['answer'] in answer

    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        user = api.user.get_user()

        query = 'INSERT INTO `submissions` (`uid`, `qid`, `answer`, `points`) VALUES (%s, %s, %s, %s);'
        args = (user['uid'], question['qid'], answer, question['success'] if correct else -question['failure'])

        cursor.execute(query, args)
    finally:
        if cursor: cursor.close()

    if correct:
        return WebSuccess('Correct!')
    else:
        return WebError('Incorrect')

def get_question(num=None, name=None, qid=None):
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

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
    finally:
        if cursor:
            cursor.close()
