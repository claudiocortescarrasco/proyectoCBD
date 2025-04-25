from django.apps import AppConfig
from neomodel import config
from django.conf import settings


class AppConfigCBD(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        config.DATABASE_URL = settings.NEOMODEL_NEO4J_BOLT_URL
