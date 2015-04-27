
import api
import uuid

import pymysql

mysql_config = {
}

__conn = None

def get_conn():
    if __conn:
        if __conn.is_connected():
            return __conn
        else:
            __conn.close()
    __conn = pymysql.connect(**mysql_config)
    return __conn

def token():
    return str(uuid.uuid4().hex)

class APIException(Exception):
    """
    Exception thrown by the API.
    """
    data = {}


def WebSuccess(message=None, data=None):
    """
    Successful web request wrapper.
    """

    return {
        "status": 1,
        "message": message,
        "data": data
    }

def WebError(message=None, data=None):
    """
    Unsuccessful web request wrapper.
    """

    return {
        "status": 0,
        "message": message,
        "data": data
    }

class WebException(APIException):
    """
    Errors that are thrown that need to be displayed to the end user.
    """

    def __init__(self, *args, data={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

class InternalException(APIException):
    """
    Exceptions thrown by the API constituting mild errors.
    """

    pass

class SevereInternalException(InternalException):
    """
    Exceptions thrown by the API constituting critical errors.
    """

    pass

def validate(schema, data):
    try:
        schema(data)
    except MultipleInvalid as inv:
        raise APIException(0, None, inv.msg)

def safe_fail(f, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except:
        return None

def flat_multi(multidict):
    flat = {}
    for key, values in multidict.items():
        flat[key] = values[0] if type(values) == list and len(values) == 1 else values
    return flat

