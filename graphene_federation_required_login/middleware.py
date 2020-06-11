import json
from django.conf import settings
import logging
logger = logging.getLogger(__name__)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        _GRAPHENE_FEDERATION_HEADER = getattr(settings,'GRAPHENE_FEDERATION_HEADER','Graphene-Federation-Header')
        setattr(info.context, _GRAPHENE_FEDERATION_HEADER, None)
        if _GRAPHENE_FEDERATION_HEADER in info.context.headers:
            setattr(info.context, _GRAPHENE_FEDERATION_HEADER, json.loads(info.context.headers[_GRAPHENE_FEDERATION_HEADER]))
        return next(root, info, **kwargs)