
import api
import uuid

import pymysql

from voluptuous import MultipleInvalid, Invalid

mysql_config = {
}

__conn = None

def get_conn():
    global __conn
    if __conn:
        try:
            __conn.ping()
            return __conn
        except:
            pass

    decoders = pymysql.converters.decoders

    for k, v in decoders.items():
        if v == pymysql.converters.Decimal:
            decoders[k] = int

    __conn = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, conv=decoders, **mysql_config)
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

def join_kwargs(data, **kwargs):
    joined = {}
    for k, v in kwargs.items():
        if v:
            joined[k] = v
        elif k in data:
            joined[k] = data[k]
    return joined

def check(*callback_tuples):
    """
    Voluptuous wrapper function to raise our APIException
    Args:
        callback_tuples: a callback_tuple should contain (status, msg, callbacks)
    Returns:
        Returns a function callback for the Schema
    """

    def v(value):
        """
        Trys to validate the value with the given callbacks.
        Args:
            value: the item to validate
        Raises:
            APIException with the given error code and msg.
        Returns:
            The value if the validation callbacks are satisfied.
        """

        for msg, callbacks in callback_tuples:
            for callback in callbacks:
                try:
                    result = callback(value)
                    if not result and type(result) == bool:
                        raise Invalid()
                except Exception:
                    raise WebException(msg)
        return value
    return v
