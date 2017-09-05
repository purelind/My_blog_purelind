from functools import wraps

from flask import g

from .errors import forbidden


def permission_required(permission):
    def decorator(f):
        # 函数也是对象，拥有__name__属性，这里将原始函数的__name__等
        # 属性复制到decorated_function()函数中
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
