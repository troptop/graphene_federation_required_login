
from . import exceptions
from functools import wraps
from django.conf import settings
from .apps import DEFAULT_GRFL_DJANGO_CONTEXT , SETTINGS_GRFL_DJANGO_CONTEXT_ATTRIBUTE

def required_federation_login(_func=None, *, header=getattr(settings,SETTINGS_GRFL_DJANGO_CONTEXT_ATTRIBUTE,DEFAULT_GRFL_DJANGO_CONTEXT)):
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