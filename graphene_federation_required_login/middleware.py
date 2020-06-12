import json
from django.conf import settings
from .apps import (DEFAULT_GFRL_DJANGO_CONTEXT , DEFAULT_GFRL_FEDERATION_HEADER ,
SETTINGS_GFRL_FEDERATION_HEADER_ATTRIBUTE , SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE)
import logging
logger = logging.getLogger(__name__)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        gfrl_federation_header = getattr(settings,SETTINGS_GFRL_FEDERATION_HEADER_ATTRIBUTE,DEFAULT_GFRL_FEDERATION_HEADER)
        gfrl_django_context = getattr(settings,SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE,DEFAULT_GFRL_DJANGO_CONTEXT)
        setattr(info.context, gfrl_django_context, None)
        if gfrl_federation_header in info.context.headers:
            setattr(info.context, gfrl_django_context, json.loads(info.context.headers[gfrl_federation_header]))
        return next(root, info, **kwargs)