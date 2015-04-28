
import api
import bcrypt
import pymysql

from voluptuous import Schema, Required, Length
from flask import request, session

from api.common import safe_fail, get_conn, InternalException, WebException, check, validate, join_kwargs

login_schema = Schema({
    Required('username'): check(
        ('Usernames must be between 3 and 50 characters', [str, Length(min=3, max=50)]),
    ),
    Required('password'): check(
        ('Passwords must be between 3 and 50 characters', [str, Length(min=3, max=50)]),
    ),
})

def is_logged_in():
    return 'uid' in session

def logout():
    session.permanent = False
    session.clear()

def get_user_scores(uid=None):
    if not uid:
        if 'uid' not in session:
            raise InternalException('Need uid to get scores')
        uid = session['uid']

    with get_conn() as cursor:
        query = ('SELECT SUM(`submissions`.`points`) AS `score`, MAX(`questions`.`num`) AS `num`'
                ' FROM `submissions` INNER JOIN `questions` ON `submissions`.`qid` = `questions`.`qid`'
                ' WHERE `uid` = %s;')
        args = (uid,)

        cursor.execute(query, args)
        scores = cursor.fetchone()
        scores['num'] = scores['num'] or 0
        scores['score'] = scores['score'] or 0
        return scores

def login(username=None, password=None, data=None):
    data = join_kwargs(data, username=username, password=password)

    validate(login_schema, data)

    username = data.pop('username')
    password = data.pop('password')

    user = safe_fail(get_user, name=username)

    if user is not None and confirm_password(password, user['password_hash']):
        if user['uid'] is not None:
            session['uid'] = user['uid']
            session.permanent = True
        else:
            raise WebException('Login error')
    else:
        raise WebException('Username or password incorrect')

def create_user(username=None, password=None, data=None):
    data = join_kwargs(data, username=username, password=password)

    validate(login_schema, data)

    username = data.pop('username')
    password = data.pop('password')

    uid = api.common.token()

    with get_conn() as cursor:
        query = 'INSERT INTO `users` (`uid`, `username`, `password_hash`) VALUES (%s, %s, %s);'

        try:
            cursor.execute(query, (uid, username, hash_password(password)))
        except pymysql.err.IntegrityError as e:
            raise WebException('User already exists')

        return uid

def get_user(uid=None, name=None):
    query = 'SELECT * FROM `users` WHERE '
    wheres = []
    if name:
        wheres.append(('`username` = %s', name))
    if uid or 'uid' in session:
        wheres.append(('`uid` = %s', uid or session['uid']))
    if not wheres:
        raise InternalException('Required to specify query')

    clauses, args = zip(*wheres)
    query += ' AND '.join(clauses)

    with get_conn() as cursor:
        cursor.execute(query, tuple(args))

        return cursor.fetchone()

def hash_password(password):
    """
    Hash plaintext password.
    Args:
        password: plaintext password
    Returns:
        Secure hash of password.
    """

    return bcrypt.hashpw(password, bcrypt.gensalt(8))

def confirm_password(attempt, password_hash):
    """
    Verifies the password attempt
    Args:
        attempt: the password attempt
        password_hash: the real password pash
    """

    return bcrypt.checkpw(attempt, password_hash)
