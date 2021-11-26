# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Advertencias(models.Model):
    id_advertencias = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=500)
    id_funcionario = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='id_funcionario')
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')

    class Meta:
        managed = False
        db_table = 'advertencias'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    cpf_cnpj = models.CharField(max_length=20)
    data_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=2, blank=True, null=True)
    email = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Clienteconvidado(models.Model):
    id_teste = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clienteConvidado'


class Convidados(models.Model):
    id_convidado = models.AutoField(primary_key=True)
    email = models.CharField(max_length=40)
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'convidados'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Equipamentoreserva(models.Model):
    id_equipamentoreserva = models.AutoField(primary_key=True)
    preco_locacao_equipamento = models.FloatField()
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')
    id_equipamento = models.ForeignKey('Equipamentos', models.DO_NOTHING, db_column='id_equipamento')
    id_pagamento = models.ForeignKey('Pagamento', models.DO_NOTHING, db_column='id_pagamento', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipamentoReserva'


class Equipamentos(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20)
    descriþÒo = models.CharField(max_length=100)
    preco = models.FloatField()
    status_equipamento = models.IntegerField()
    data_ultima_alteracao = models.DateTimeField()
    ultima_alteracao = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipamentos'


class Espacos(models.Model):
    id_espaco = models.AutoField(primary_key=True)
    status_espaco = models.IntegerField(blank=True, null=True)
    vagas = models.IntegerField(blank=True, null=True)
    data_ultima_alteracao = models.DateTimeField(blank=True, null=True)
    id_tipo_espaco = models.ForeignKey('Tipoespaco', models.DO_NOTHING, db_column='id_tipo_espaco')
    ultima_alteracao = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    imagem = models.TextField(blank=True, null=True)
    preco = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'espacos'


class Funcionarios(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    cpf_cnpj = models.CharField(max_length=14)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=2, blank=True, null=True)
    email = models.CharField(max_length=40)
    telefone = models.CharField(max_length=20)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=12)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funcionarios'


class Pacotehoras(models.Model):
    id_pacote_horas = models.AutoField(primary_key=True)
    qtd_horas = models.IntegerField()
    status_pacotehoras = models.IntegerField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_empresa = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_empresa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pacoteHoras'


class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    metodo = models.CharField(max_length=45)
    cod_mercadopago = models.IntegerField()
    status_pagamento = models.IntegerField()
    datahora_log = models.DateTimeField()
    id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva', blank=True, null=True)
    id_equipamento = models.ForeignKey(Equipamentos, models.DO_NOTHING, db_column='id_equipamento', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagamento'


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    data_reserva = models.DateField()
    is_aluguel = models.PositiveIntegerField(blank=True, null=True)
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    hora_limpeza = models.TimeField()
    datahora_log = models.DateTimeField(blank=True, null=True)
    hora_entrada_real = models.TimeField(blank=True, null=True)
    hora_saida_real = models.TimeField(blank=True, null=True)
    hora_limpeza_real = models.TimeField(blank=True, null=True)
    preco_total = models.FloatField(blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_espaco = models.ForeignKey(Espacos, models.DO_NOTHING, db_column='id_espaco')
    id_pacote_horas = models.ForeignKey(Pacotehoras, models.DO_NOTHING, db_column='id_pacote_horas', blank=True, null=True)
    hash_qrcode = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reserva'


class Tipoespaco(models.Model):
    id_tipoespaco = models.AutoField(db_column='id_tipoEspaco', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(max_length=200, blank=True, null=True)
    nome = models.CharField(max_length=45)
    tempo_limpeza = models.TimeField(blank=True, null=True)
    preco = models.FloatField(blank=True, null=True)
    data_ultima_alteracao = models.DateTimeField(blank=True, null=True)
    compartilhado = models.PositiveIntegerField()
    ultima_alteracao = models.ForeignKey(Funcionarios, models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    imagem = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipoEspaco'
