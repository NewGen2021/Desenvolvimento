import json

from cria_coworking.models import Administrador
from custom_templates.models import *
from django.core.management.base import BaseCommand
from domains.models import Domain


class NotRunningInTTYException(Exception):
    pass


class Command(BaseCommand):
    help = 'Used to update json domains.'
    stealth_options = ('stdin',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DomainModel = Domain

    def handle(self, *args, **options):
        domains = self.DomainModel.objects.all()
        domain_json = {}

        for domain in domains:
            try:
                database = Administrador.objects.using('default').get(domain=domain.id).database
            except Administrador.DoesNotExist:
                database = 'default'
            finally:
                domain_json[domain.domain] = {'domain': domain.domain, 'name': domain.name, 'isActive': domain.isActive,
                                              'database': database}
        f = open('local/domain.json', 'w')
        f.write(str(json.dumps(domain_json)))
        self.stdout.write("\"local/domain.json\" foi sincronizado com o banco de dados com sucesso.")
        f.close()
