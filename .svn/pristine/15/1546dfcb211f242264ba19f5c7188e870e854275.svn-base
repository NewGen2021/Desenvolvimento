from django.apps import AppConfig
from django.core.management import call_command
from django.conf import settings


class DomainsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domains'
    def ready(self):
        call_command('updatejsondomain')
        # if settings.AUTOMATIC_TEST:
        #     call_command('loaddata', 'tests/fixures/cria_coworking.json')
        #     call_command('loaddata', 'tests/fixures/custom_templates.json')
        #     call_command('loaddata', 'tests/fixures/domains.json')
            