from django.db import models
from domains.models import Domain
import gere_coworking.models.models_choice as c
from django.utils.translation import gettext as _
import sys

availableDomains = Domain.objects.filter(isActive=0)

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
    database = models.CharField(max_length=128)
    domain = models.ForeignKey(Domain, models.DO_NOTHING, db_column='domain', blank=True, null=True)

    class Meta:
        db_table = 'administrador'
