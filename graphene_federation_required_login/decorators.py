
from . import exceptions
from functools import wraps

def required_federation_login(_func=None, *, header='gateway'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, info, **kwargs):
            if hasattr(info.context,header) and getattr(info.context,header):
                return view_func(self, info, **kwargs)
            raise exceptions.PermissionDenied()
        return _wrapped_view
    if _func is None:
        return decorator
    else:
        return decorator(_func)