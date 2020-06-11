import json
from django.conf import settings
from .apps import (DEFAULT_GRFL_DJANGO_CONTEXT , DEFAULT_GRFL_FEDERATION_HEADER ,
SETTINGS_GRFL_FEDERATION_HEADER_ATTRIBUTE , SETTINGS_GRFL_DJANGO_CONTEXT_ATTRIBUTE)
import logging
logger = logging.getLogger(__name__)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        logger.error('-------  HEADER ------- {}'.format(info.context.headers.items()))
        grfl_federation_header = getattr(settings,SETTINGS_GRFL_FEDERATION_HEADER_ATTRIBUTE,DEFAULT_GRFL_FEDERATION_HEADER)
        grfl_django_context = getattr(settings,SETTINGS_GRFL_DJANGO_CONTEXT_ATTRIBUTE,DEFAULT_GRFL_DJANGO_CONTEXT)
        logger.error('-------  grfl_federation_header ------- {}'.format(grfl_federation_header))
        setattr(info.context, grfl_django_context, None)
        logger.error('-------  _GETATTRIBUTE ------- {}'.format(getattr(info.context, grfl_django_context,"NOT WORKING")))
        if grfl_federation_header in info.context.headers:
            setattr(info.context, grfl_django_context, json.loads(info.context.headers[grfl_federation_header]))
            logger.error('-------  MIDDLEWARE ------- {}'.format(dir(info.context)))
            logger.error('-------  MIDDLEWARE ------- {}'.format(info.context.__dict__[grfl_django_context]))
        return next(root, info, **kwargs)