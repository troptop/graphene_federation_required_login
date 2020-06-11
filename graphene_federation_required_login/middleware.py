import json
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        logger.error('-------  HEADER ------- {}'.format(info.context.headers.items()))
        _GRAPHENE_FEDERATION_HEADER = getattr(settings,'GRAPHENE_FEDERATION_HEADER','Graphene-Federation-Header')
        logger.error('-------  _GRAPHENE_FEDERATION_HEADER ------- {}'.format(_GRAPHENE_FEDERATION_HEADER))
        setattr(info.context, _GRAPHENE_FEDERATION_HEADER, None)
        logger.error('-------  _GETATTRIBUTE ------- {}'.format(getattr(info.context, _GRAPHENE_FEDERATION_HEADER,"NOT WORKING")))
        if _GRAPHENE_FEDERATION_HEADER in info.context.headers:
            setattr(info.context, _GRAPHENE_FEDERATION_HEADER, json.loads(info.context.headers[_GRAPHENE_FEDERATION_HEADER]))
            logger.error('-------  MIDDLEWARE ------- {}'.format(dir(info.context)))
        return next(root, info, **kwargs)