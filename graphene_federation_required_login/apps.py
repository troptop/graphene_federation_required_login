from django.apps import AppConfig

DEFAULT_GFRL_DJANGO_CONTEXT = 'gfrl'
DEFAULT_GFRL_FEDERATION_HEADER = 'Gfrl-Federation-Header'
SETTINGS_GFRL_FEDERATION_HEADER_ATTRIBUTE = 'GFRL_FEDERATION_HEADER'
SETTINGS_GFRL_DJANGO_CONTEXT_ATTRIBUTE = 'GFRL_DJANGO_CONTEXT'
class GrapheneFederationRequiredLoginConfig(AppConfig):
    name = 'graphene_federation_required_login'
