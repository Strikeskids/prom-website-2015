
def error_message(error):
    return error.args[0]

def api_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        web_result = {}
        try:
            web_result = f(*args, **kwargs)
        except WebException as e:
            web_result = WebError(error_message(e), e.data)
        except InternalException as e:
            message = error_message(e)
            if type(e) == SevereInternalException:
                web_result = WebError('There was a critical internal error. Contact administrator')
            else:
                web_result = WebError(message)
        except Exception as e:
            web_result = WebError('Failed because of %s'%(type(e)))

        return json.dumps(web_result)

    return wrapper

def require_login(f):
    """
    Wraps routing functions that require a user to be logged in
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        if not api.user.is_logged_in():
            raise WebException("You must be logged in")
        return f(*args, **kwds)
    return wrapper

def check_csrf(f):
    @wraps(f)
    @require_login
    def wrapper(*args, **kwds):
        if 'token' not in session:
            raise InternalException("CSRF token not in session")
        if 'token' not in request.form:
            raise InternalException("CSRF token not in form")
        if session['token'] != request.form['token']:
            raise InternalException("CSRF token is not correct")
        return f(*args, **kwds)
    return wrapper
