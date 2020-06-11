import json
from django.conf import settings
from .apps import (DEFAULT_GFRL_DJANGO_CONTEXT , DEFAULT_GFRL_FEDERATION_HEADER ,
SETTINGS_GFRL_FEDERATION_HEADER_ATTRIBUTE , SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE)
import logging
logger = logging.getLogger(__name__)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        logger.error('-------  HEADER ------- {}'.format(info.context.headers.items()))
        gfrl_federation_header = getattr(settings,SETTINGS_GFRL_FEDERATION_HEADER_ATTRIBUTE,DEFAULT_GFRL_FEDERATION_HEADER)
        gfrl_django_context = getattr(settings,SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE,DEFAULT_GFRL_DJANGO_CONTEXT)
        logger.error('-------  gfrl_federation_header ------- {}'.format(gfrl_federation_header))
        setattr(info.context, gfrl_django_context, None)
        logger.error('-------  _GETATTRIBUTE ------- {}'.format(getattr(info.context, gfrl_django_context,"NOT WORKING")))
        if gfrl_federation_header in info.context.headers:
            setattr(info.context, gfrl_django_context, json.loads(info.context.headers[gfrl_federation_header]))
            logger.error('-------  MIDDLEWARE ------- {}'.format(dir(info.context)))
            logger.error('-------  MIDDLEWARE ------- {}'.format(info.context.__dict__[gfrl_django_context]))
        return next(root, info, **kwargs)