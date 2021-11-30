from django.db import models
from domains.models import Domain
import common.models_choices as c
from django.utils.translation import gettext as _
import sys

availableDomains = Domain.objects.filter(isActive=0)

class AdministradorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).using('default')

class Administrador(models.Model):
    """ nome = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    cnpj = models.CharField(max_length=20, null=False, verbose_name=_("CPF"))
    telefone = models.CharField(max_length=128)
    nome = models.CharField(max_length=128)
    email = models.EmailField(null=False, verbose_name=_("E-mail"), max_length=40)
    telefone = models.CharField(null=False, verbose_name=_("Telefone"), max_length=20)
    cep = models.CharField(max_length=12)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(null=False, choices=c.ESTADO_CHOICES, max_length=2)
    dominio = models.ForeignKey(Domain, models.DO_NOTHING, db_column='domain', blank=True, null=True)
    database = models.CharField(max_length=128)     """

    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=128)
    cnpj = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20)
    cep = models.CharField(max_length=12)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    database = models.CharField(max_length=128, blank=True, null=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING, db_column='domain', blank=True, null=True)
    plano = models.CharField(max_length=45, blank=True, null=True)
    validade_plano = models.DateTimeField(blank=True, null=True)
    
    def get_formatted_cnpj(self):
        if len(self.cnpj) != 14:
            return self.cnpj
        else:
            # 84.584.110/0001-38
            cnpj = self.cnpj
            return "%s.%s.%s/%s-%s" %(cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])
    
    # def get_clean_cnpj(self):
    #     # return self.cnpj
    #     return '%s'.replace('.', '').replace('/', '').replace('-', '') %self.cnpj

    def has_plano(self):
        if self.plano:
            return True
        return False
        
    def get_plano(self):
        if self.plano:
            return self.plano
        return 'Nenhum plano selecionado'

    def get_database(self):
        if self.database:
            return self.database
        return 'Nenhum banco de dados encontrado'

    # def has_system_and_not_plan(self):
    #     active_plan = self.plano or self.plano
    #     if self.database != None
    
    def get_validade_plano(self):
        if self.validade_plano:
            return self.validade_plano
        else:
            return '--/--/--'
    
    objects = AdministradorManager()
    class Meta:
        db_table = 'administrador'
