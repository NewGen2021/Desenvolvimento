from django.apps import AppConfig
from django.core.management import call_command


class DomainsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domains'
    def ready(self):
        call_command('updatejsondomain')