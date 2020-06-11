import json
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        _GRAPHENE_FEDERATION_HEADER = getattr(settings,'GRAPHENE_FEDERATION_HEADER','GRAPHENE_FEDERATION_HEADER')
        if settings.DEBUG:
            logger.error('graphene_federation_required_login - middleware : {}'.format(info.context.headers.items()))
        setattr(info.context, _GRAPHENE_FEDERATION_HEADER, None)
        if 'user' in info.context.headers:
            #logger.error('-------  USER ------- {}'.format(info.context.headers['user']))
            setattr(info.context, _GRAPHENE_FEDERATION_HEADER, json.loads(info.context.headers[_GRAPHENE_FEDERATION_HEADER]))
        if settings.DEBUG:
            logger.error('graphene_federation_required_login - middleware : {}'.format(getattr(info.context,_GRAPHENE_FEDERATION_HEADER)))        
        return next(root, info, **kwargs)