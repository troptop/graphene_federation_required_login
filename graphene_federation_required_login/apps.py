from django.apps import AppConfig

DEFAULT_GRFL_DJANGO_CONTEXT = 'grfl'
DEFAULT_GRFL_FEDERATION_HEADER = 'Grfl-Federation-Header'
SETTINGS_GRFL_FEDERATION_HEADER_ATTRIBUTE = 'GRFL_FEDERATION_HEADER'
SETTINGS_GRFL_DJANGO_CONTEXT_ATTRIBUTE = 'GRFL_DJANGO_CONTEXT'
class GrapheneFederationRequiredLoginConfig(AppConfig):
    name = 'graphene_federation_required_login'
