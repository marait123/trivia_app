from flask import abort, request
from functools import wraps


def UnexpectedArgumentHandler(expected_arguments):
    def wrap(f):
        @wraps(f)
        def wrapped_f(*args):
            for argument in request.args:
                if not argument in expected_arguments:
                    abort(400)
            return f(*args)
        return wrapped_f
    return wrap
