
from . import exceptions
from functools import wraps
from django.conf import settings
from .apps import (DEFAULT_GFRL_DJANGO_CONTEXT , SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE)
def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index('info')]
            return func(info, *args, **kwargs)
        return wrapper
    return decorator

def required_federation_login(_func=None, *, header=getattr(settings,SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE,DEFAULT_GFRL_DJANGO_CONTEXT)):
    def decorator(view_func):
        @wraps(view_func)
        @context(view_func)
        def _wrapped_view(self, info, **kwargs):
            if hasattr(info.context,header) and getattr(info.context,header):
                return view_func(self, info, **kwargs)
            raise exceptions.PermissionDenied()
        return _wrapped_view
    if _func is None:
        return decorator
    else:
        return decorator(_func)