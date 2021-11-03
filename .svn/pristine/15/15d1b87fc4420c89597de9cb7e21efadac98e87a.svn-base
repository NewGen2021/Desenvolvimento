import sys, json
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.utils.text import capfirst
from domains.models import Domain
from cria_coworking.models import Administrador


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
                domain_json[domain.domain] = {'domain': domain.domain,'name':domain.name, 'isActive': domain.isActive,
                'database': database}
        f = open('local/domain.json', 'w')
        f.write(str(json.dumps(domain_json)))
        self.stdout.write("\"local/domain.json\" foi sincronizado com o banco de dados com sucesso.")
        f.close()
