from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db.models.fields.related import OneToOneField
from django.utils.translation import gettext as _
from django.conf import settings
import datetime
# import gere_coworking.models_helper as h     # 'h' de "Helper"
import common.models_choices as c     # 'c' de "Choice"


class FuncionariosModel(models.Model):
    SEXO_CHOICES = c.SEXO_CHOICES
    ESTADO_CHOICES = c.ESTADO_CHOICES

    id_funcionario = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=60)
    cpf_cnpj = models.CharField(max_length=14, null=False, verbose_name=_("CPF"))
    data_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(null=True, verbose_name=_("Gênero"), choices=SEXO_CHOICES, max_length=2)
    email = models.EmailField(null=False, verbose_name=_("E-mail"), max_length=40)
    telefone = models.CharField(null=False, verbose_name=_("Telefone"), max_length=20)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(null=False, choices=ESTADO_CHOICES, max_length=2)
    cep = models.CharField(max_length=12)
    # senha = models.CharField(null=False, max_length=120, validators=[MinLengthValidator(6)])

    # objects = h.GerenciaPessoas()

    class Meta:
        managed = False
        db_table = 'funcionarios'

#Validação: ok
class ClienteModel(models.Model):
    SEXO_CHOICES = c.SEXO_CHOICES
    ESTADO_CHOICES = c.ESTADO_CHOICES
    
    id_cliente = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=60)
    cpf_cnpj = models.CharField(max_length=20, null=False, verbose_name=_("CPF"))
    data_nascimento = models.DateField(blank=True, null=True)
    genero = models.CharField(null=True, verbose_name=_("Gênero"), choices=SEXO_CHOICES, max_length=2)
    email = models.EmailField(null=False, verbose_name=_("E-mail"), max_length=40)
    telefone = models.CharField(null=False, verbose_name=_("Telefone"), max_length=20)
    logradouro = models.CharField(max_length=45)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=35)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(null=False, choices=ESTADO_CHOICES, max_length=2)
    cep = models.CharField(max_length=9)
    # senha = models.CharField(null=False, max_length=120, validators=[MinLengthValidator(6)])

    # objects = h.GerenciaPessoas()

    class Meta:
        managed = False
        db_table = 'cliente'

class TipoespacoModel(models.Model):

    id_tipoespaco = models.AutoField(db_column='id_tipoEspaco', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(max_length=200, blank=True, null=True)
    nome = models.CharField(max_length=45)
    ultima_alteracao = models.ForeignKey(FuncionariosModel, models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    tempo_limpeza = models.TimeField(blank=True, null=True)
    preco = models.FloatField(blank=True, null=True)
    data_ultima_alteracao = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    compartilhado = models.PositiveIntegerField()
    imagem = models.ImageField(null=True, blank=True, upload_to="", default="default/espaco_default.jpg")

    class Meta:
        managed = False
        db_table = 'tipoEspaco'
    
    def get_descricao_breve(self):
        TAMANHO_MAX_DESCRICAO: int = 70
        return f"{self.descricao[:TAMANHO_MAX_DESCRICAO]}..." if len(self.descricao) >= TAMANHO_MAX_DESCRICAO else self.descricao
    
    def get_tempo_limpeza(self):
        if self.tempo_limpeza >= datetime.time(1, 0, 0):
            return _(f"%s hr{'s' if self.tempo_limpeza.hour != 1 else ''}") % self.tempo_limpeza.hour
        elif self.tempo_limpeza >= datetime.time(0, 1, 0):
            return _(f"%s min{'s' if self.tempo_limpeza.minute != 1 else ''}") % self.tempo_limpeza.minute
        else:
            return _(f"%s seg{'s' if self.tempo_limpeza.second != 1 else ''}") % self.tempo_limpeza.second
    
    def get_preco(self):
        preco_formatado = f"R$ {self.preco:.2f}".replace('.', ',')
        return f"{preco_formatado:>13}"
    
    def get_compartilhado(self):
        return _("SIM") if self.compartilhado else _("NÃO")
    
    def __str__(self):
        return str(f'{self.nome}')#GA BRIELP
    

class EquipamentosModel(models.Model):

    STATUS_CHOICES = c.EQUIPAMENTOS_STATUS_CHOICES

    id_equipamento = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20)
    descrição = models.CharField(max_length=100)
    preco = models.FloatField()
    ultima_alteracao = models.ForeignKey(FuncionariosModel, models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    # ultima_alteracao = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='id_funcionario')
    status_equipamento = models.IntegerField(choices=STATUS_CHOICES)
    data_ultima_alteracao = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'equipamentos'
    

class PacotehorasModel(models.Model):
    id_pacote_horas = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(ClienteModel, models.DO_NOTHING, db_column='id_cliente', related_name='pacote_id_cliente')
    qtd_horas = models.IntegerField()
    id_empresa = models.ForeignKey(ClienteModel, models.DO_NOTHING, db_column='id_empresa', blank=True, null=True, related_name='pacote_id_empresa')
    status_pacotehoras = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pacoteHoras'

class EspacosModel(models.Model):
    STATUS_CHOICES = c.ESPACOS_STATUS_CHOICES

    ''' CRIAR POSTERIORMENTE CAMPO DE DESCRIÇÃO '''
    id_espaco = models.AutoField(primary_key=True)
    id_tipo_espaco = models.ForeignKey(TipoespacoModel, models.DO_NOTHING, db_column='id_tipo_espaco', blank=False, null=False)
    # id_tipo_espaco = models.ForeignKey('Tipoespaco', models.DO_NOTHING, db_column='id_tipo_espaco')
    ultima_alteracao = models.ForeignKey(FuncionariosModel, models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    # ultima_alteracao = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    status_espaco = models.IntegerField(blank=True, null=True)
    vagas = models.IntegerField(blank=True, null=True)
    data_ultima_alteracao = models.DateTimeField(blank=True, null=True)
    imagem = models.ImageField(null=True, blank=True, upload_to="", default="default/espaco_default.jpg")
    preco = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(f'{self.id_tipo_espaco.nome}')#GABRIEL

    class Meta:
        managed = False
        db_table = 'espacos'
    
    def get_status(self):
        return _("Ativado") if self.status_espaco else _("Desativado")
    
    def get_vagas(self):
        return self.vagas if self.vagas else _("Indefinido")
    
    def get_preco(self):
        if self.preco is None:
            self.preco = self.id_tipo_espaco.preco
        preco_formatado = f"R$ {self.preco:.2f}".replace('.', ',')
        return f"{preco_formatado:>13}"
    
    def get_tipo_espaco(self):
        return self.id_tipo_espaco.nome
    
    def get_image_url(self):
        # return 'batata'
        return "%s%s" %(settings.MEDIA_URL, self.imagem.decode('utf-8'))
    
    def status(self):
        return _("Ativado") if self.status else _("Desativado")

class AdvertenciasModel(models.Model):
    id_advertencias = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=500)
    id_reserva = models.ForeignKey('ReservaModel', models.DO_NOTHING, db_column='id_reserva')
    id_funcionario = models.ForeignKey(FuncionariosModel, models.DO_NOTHING, db_column='domain', blank=True, null=True)
    # id_funcionario = models.ForeignKey('FuncionariosModel', models.DO_NOTHING, db_column='id_funcionario')

    class Meta:
        managed = False
        db_table = 'advertencias'

class PagamentoModel(models.Model):
    METODO_CHOICES = c.PAGAMENTO_METODO_CHOICES
    STATUS_CHOICES = c.PAGAMENTO_STATUS_CHOICES

    id_pagamento = models.AutoField(primary_key=True)
    metodo = models.CharField(max_length=45, choices=METODO_CHOICES)
    cod_mercadopago = models.IntegerField()
    status_pagamento = models.IntegerField(choices=STATUS_CHOICES)
    datahora_log = models.DateTimeField(auto_now_add=True)
    # id_reserva = models.ForeignKey('ReservaModel', models.DO_NOTHING, db_column='id_reserva')
    id_equipamento = models.ForeignKey('EquipamentosModel', models.DO_NOTHING, db_column='id_equipamento', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagamento'

class ReservaModel(models.Model):

    id_reserva = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(ClienteModel, models.DO_NOTHING, db_column='id_cliente')
    id_pagamento = models.ForeignKey(PagamentoModel, models.DO_NOTHING, db_column='id_pagamento', blank=True, null=True)
    is_aluguel = models.PositiveIntegerField(blank=True, null=True)
    id_espaco = models.ForeignKey(EspacosModel, models.DO_NOTHING, db_column='id_espaco')
    id_pacote_horas = models.ForeignKey(PacotehorasModel, models.DO_NOTHING, db_column='id_pacote_horas', blank=True, null=True)
    data_reserva = models.DateField()
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    hora_limpeza = models.TimeField()
    datahora_log = models.DateTimeField(blank=True, null=True)
    hora_entrada_real = models.TimeField(blank=True, null=True)
    hora_saida_real = models.TimeField(blank=True, null=True)
    hora_limpeza_real = models.TimeField(blank=True, null=True)
    preco_total = models.FloatField(blank=True, null=True)
    hash_qrcode = models.CharField(max_length=32, blank=True, null=True)


    # objects = h.GerenciaReserva()

    class Meta:
        managed = False
        db_table = 'reserva'

class EquipamentoreservaModel(models.Model):
    
    id_reserva = models.OneToOneField('ReservaModel', models.DO_NOTHING, db_column='id_reserva', primary_key=True)
    id_equipamento = models.ForeignKey('EquipamentosModel', models.DO_NOTHING, db_column='id_equipamento')
    preco_locacao_equipamento = models.FloatField()
    id_pagamento = models.ForeignKey('PagamentoModel', models.DO_NOTHING, db_column='id_pagamento')

    class Meta:
        managed = False
        db_table = 'equipamentoReserva'
        unique_together = (('id_reserva', 'id_equipamento'),)

class ConvidadosModel(models.Model):
    id_convidado = models.AutoField(primary_key=True)
    # id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='id_reserva')
    id_reserva = models.ForeignKey(ReservaModel, models.DO_NOTHING, db_column='id_reserva', blank=True, null=True)
    id_cliente = models.ForeignKey(ClienteModel, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    email = models.EmailField(null=False, verbose_name="E-mail", max_length=40)

    class Meta:
        managed = False
        db_table = 'convidados'