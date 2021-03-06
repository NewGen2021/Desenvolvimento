# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Administrador(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=128)
    email = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20)
    cep = models.CharField(max_length=12)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    database = models.CharField(max_length=128)
    domain = models.ForeignKey('Domain', models.DO_NOTHING, db_column='domain', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrador'
        app_label = 'cria_coworking'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Domain(models.Model):
    id = models.BigAutoField(primary_key=True)
    domain = models.CharField(unique=True, max_length=128)
    name = models.CharField(max_length=128)
    isactive = models.IntegerField(db_column='isActive')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'domain'
        app_label = 'cria_coworking'
