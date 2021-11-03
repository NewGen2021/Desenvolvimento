from django.contrib.auth.backends import UserModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMultiAlternatives
from django.forms.widgets import Widget
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _

from crispy_forms.helper import FormHelper
from cria_coworking.forms import _unicode_ci_compare

from gere_coworking.models import *
from common.models_choices import *
from common.form_fields_verifiers.cpfVerifier import *
from common.form_fields_verifiers.cnpjVerifier import *
from common.form_fields_verifiers.phoneVerifier import *
from common.form_fields_verifiers.dateVerifier import *
from common.form_fields_verifiers.cepVerifier import *

from common import forms_util as h
from common.form_fields_verifiers.cnpjVerifier import formatCNPJ
from common.form_fields_verifiers.cpfVerifier import formatCpf
import common.form_fields_verifiers.cardNumberVerifier as card_verifier
import common.form_fields_verifiers.dateVerifier as date_verifier

import sys



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label=_("CPF/CNPJ"))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true'}), label=_('Senha'))
    
    # class Meta:
    #     model= User
    #     fields= ["username", "password"]


    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
        
    #     username = formatCNPJ(username)
    #     username = formatCpf(username)
        
    #     print('--------------------- USERNAME 2222222222 ')
    #     print(username, password, file=sys.stderr)
        
    #     if username is not None and password:
    #         self.user_cache = authenticate(self.request, username=username, password=password)
    #         if self.user_cache is None:
    #             try:
    #                 user = User.objects.exclude(pk=self.instance.pk).get(username=username)
    #                 raise h.raise_error('Senha incorreta, tente novamente.', 'incorrect')
    #             except User.DoesNotExist:
    #                 raise h.raise_error('Usuário com o CPF informado não existe!', 'not_exists')
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
        
    #     return self.cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            return username
        except User.DoesNotExist:
            h.raise_error(_('Usuário com o CPF informado não existe!'), 'not_exists')

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise h.raise_error(_('Senha incorreta, tente novamente.'), 'incorrect')
            return password
        except User.DoesNotExist:
            h.raise_error(_('Usuário com o CPF informado não existe!'), 'not_exists')


class RegistrarAdministradorForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"70"}), label=_("Razão social"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label=_("CNPJ"))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true', 'maxlength':"70"}))
    telefone = forms.CharField(widget=forms.TextInput(
    attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'id_administrador_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_logradouro'}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"5", 'id': 'id_administrador_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_bairro'}))
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
        attrs={'required': 'true', 'id': 'id_administrador_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_cidade'}))

    class Meta:
        model= FuncionariosModel
        fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    
    # VERIFIERS
    def clean_cpf_cnpj(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cpf_cnpj"), "cnpj_administrador")
    def clean_telefone(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("telefone"), "telefone")
    def clean_cep(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cep"), "cep")
    def clean_nome(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("nome"), "nome_empresa")
    def clean_numero(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("numero"), "numero_endereco")
    # def clean_logradouro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("logradouro"), "endereco")
    # def clean_bairro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("bairro"), "endereco")
    def clean_cidade(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cidade"), "endereco")

class ClientePessoaForm(forms.ModelForm):

    # FIELDS
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"70"}), label=_("Nome Completo"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000.000.000-00"}), label=_("CPF"), max_length=11)
    data_nascimento = forms.DateField(widget=forms.TextInput(
        attrs={'data-mask': '00/00/0000', 'required': 'true'}), label=_("Data de Nascimento"))
    genero = forms.Select(
        attrs={'required': 'false'})
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true', 'maxlength':"70"}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'id_pessoa_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_pessoa_logradouro', 'maxlength':"45"}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"5", 'id': 'id_pessoa_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_pessoa_bairro', 'maxlength': '35'}))
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
        attrs={'required': 'true', 'id': 'id_pessoa_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_pessoa_cidade', 'maxlength': '30'}))
    
    # VERIFIERS
    def clean_cpf_cnpj(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cpf_cnpj"), "cpf")
    def clean_telefone(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("telefone"), "telefone")
    def clean_data_nascimento(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("data_nascimento"), "data_nascimento")
    def clean_cep(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cep"), "cep")
    def clean_nome(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("nome"), "nome")
    def clean_numero(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("numero"), "numero_endereco")
    # def clean_logradouro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("logradouro"), "endereco")
    # def clean_bairro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("bairro"), "endereco")
    def clean_cidade(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cidade"), "endereco")
    
    class Meta:
        model= ClienteModel
        fields= ["nome", "senha", "cpf_cnpj", "data_nascimento", "genero", "email", "telefone", "cep", "logradouro", "numero", "bairro", "cidade", "estado"]    


class ClienteEmpresaForm(forms.ModelForm):
    
    # FIELDS
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label=_("Razão Social"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label=_("CNPJ"))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true'}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'id_empresa_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_empresa_logradouro'}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"5", 'id': 'id_empresa_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_empresa_bairro'}))
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
        attrs={'required': 'true', 'id': 'id_empresa_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_empresa_cidade'}))

    # VERIFIERS
    def clean_cpf_cnpj(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cpf_cnpj"), "cnpj")
    def clean_telefone(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("telefone"), "telefone")
    def clean_cep(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cep"), "cep")
    def clean_nome(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("nome"), "nome_empresa")
    def clean_numero(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("numero"), "numero_endereco")
    # def clean_logradouro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("logradouro"), "endereco")
    # def clean_bairro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("bairro"), "endereco")
    def clean_cidade(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cidade"), "endereco")

    class Meta:
        model= ClienteModel
        fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "cidade", "estado"]


class FuncionariosForm(forms.ModelForm):

    # FIELDS
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"70"}), label=_("Nome Completo"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000.000.000-00"}), label=_("CPF"), max_length=11)
    data_nascimento = forms.DateField(widget=forms.TextInput(
        attrs={'data-mask': '00/00/0000', 'required': 'true'}), label=_("Data de Nascimento"))
    genero = forms.Select(
        attrs={'required': 'false'})
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true', 'maxlength':"70"}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'id_funcionario_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_funcionario_logradouro', 'maxlength':"45"}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"5", 'id': 'id_funcionario_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_funcionario_bairro', 'maxlength': '35'}))
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
        attrs={'required': 'true', 'id': 'id_funcionario_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_funcionario_cidade', 'maxlength': '30'}))

    class Meta:
        model= FuncionariosModel
        fields= ["nome", "senha", "data_nascimento", "cpf_cnpj", "genero", "email", "telefone", "cep", "logradouro", "numero", "bairro", "cidade", "estado"]
        # model= FuncionariosModel
        # fields= ["nome", "senha", "cpf_cnpj", "data_nascimento", "genero", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]
    
    # VERIFIERS
    def clean_cpf_cnpj(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cpf_cnpj"), "cpf_funcionario")
    def clean_telefone(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("telefone"), "telefone")
    def clean_data_nascimento(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("data_nascimento"), "data_nascimento")
    def clean_cep(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cep"), "cep")
    def clean_nome(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("nome"), "nome")
    def clean_numero(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("numero"), "numero_endereco")
    # def clean_logradouro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("logradouro"), "endereco")
    # def clean_bairro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("bairro"), "endereco")
    def clean_cidade(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cidade"), "endereco")
    
    


class TipoespacoForm(forms.ModelForm):
    descricao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"200"}), label=_("Obrigatório"))
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"45"}), label=_("Obrigatório"))
    preco = forms.DecimalField(widget=forms.NumberInput(
        attrs={'required': 'true'}), label=_("Obrigatório"))
    compartilhado = forms.NullBooleanField(widget=forms.CheckboxInput(), label=_("Compartilhado. (Deixe marcado se o espaço for compartilhado)"), required=False)
    tempo_limpeza = forms.TimeField(widget=forms.TimeInput(
        attrs={'required': 'true'}), label=_("hh:mm:ss | Obrigatório"))
    imagem = forms.ImageField(widget=forms.FileInput(
        attrs={'onchange': 'readURL(this.value)'}), label=_("Opcional"), required=False)
    
    class Meta:
        model= TipoespacoModel
        fields= ["nome", "compartilhado", "descricao", "tempo_limpeza", "preco", "imagem", ]

class TipoespacoLabelsForm(forms.ModelForm):
    descricao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"200", 'placeholder': _('Ex: Uma sala reservada para sua equipe.')}), label=_("Descrição"))
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"45", 'placeholder': _('Ex: Sala de reunião')}), label=_("Nome"))
    preco = forms.DecimalField(widget=forms.NumberInput(
        attrs={'required': 'true', 'placeholder': '139.99'}), label=_("Preço"))
    compartilhado = forms.NullBooleanField(widget=forms.CheckboxInput(), label=_("Compartilhado. (Deixe marcado se o espaço for compartilhado)"), required=False)
    tempo_limpeza = forms.TimeField(widget=forms.TimeInput(
        attrs={'required': 'true', 'placeholder': _('hh:mm:ss')}), label=_("Tempo limpeza"))
    imagem = forms.ImageField(widget=forms.FileInput(
        attrs={'onchange': 'readURL(this.value)'}), label=_("Imagem"), required=False)
    
    class Meta:
        model= TipoespacoModel
        fields= ["nome", "compartilhado", "descricao", "tempo_limpeza", "preco", "imagem", ]

class EquipamentosForm(forms.ModelForm):
    class Meta:
        model= EquipamentosModel
        fields= ["tipo", "descrição", "preco", "ultima_alteracao", "status_equipamento", "data_ultima_alteracao"]

class PacoteHorasForm(forms.ModelForm):
    class Meta:
        model= PacotehorasModel
        fields= ["id_cliente", "qtd_horas", "id_empresa", "status_pacotehoras"]

class EspacosForm(forms.ModelForm):
    preco = forms.DecimalField(widget=forms.NumberInput(
        attrs={'required': 'false', 'placeholder': '139.99'}), label=_("Opcional"), required=False)
    status_espaco = forms.CharField(widget=forms.Select(choices=ESPACOS_STATUS_CHOICES,
        attrs={'required': 'true', 'id': 'id_parcelas'}), label=_("Status de espaços"))
    imagem = forms.ImageField(widget=forms.FileInput(
        attrs={'onchange': 'readURL(this.value)'}), label=_("Opcional"), required=False)
    class Meta:
        model= EspacosModel
        fields= ["id_tipo_espaco", "vagas", "preco", "status_espaco", "imagem"]

class EspacosLabelsForm(forms.ModelForm):
    # id_tipo_espaco = forms.Field(widget=forms.Select(
    #     attrs={'required': 'true', 'placeholder': 'Selecione'}), label=_("Tipo de espaço"))
    vagas = forms.IntegerField(widget=forms.NumberInput(
        attrs={'required': 'true', 'placeholder': '12'}), label=_("Vagas"), required=True)
    preco = forms.DecimalField(widget=forms.NumberInput(
        attrs={'required': 'false', 'placeholder': '139.99'}), label=_("Preço"), required=False)
    status_espaco = forms.CharField(widget=forms.Select(choices=ESPACOS_STATUS_CHOICES,
        attrs={'required': 'true', 'id': 'id_parcelas', 'placeholder': _('Selecione')}), label=_("Status de espaços"))
    imagem = forms.ImageField(widget=forms.FileInput(), label=_("Imagem"), required=False)
    class Meta:
        model= EspacosModel
        fields= ["id_tipo_espaco", "vagas", "preco", "status_espaco", "imagem"]

class ReservaForm(forms.ModelForm):
    data_reserva = forms.DateField(widget=forms.TextInput(attrs={'data-mask':'00/00/0000', 'required':'true'}), label=_('Data de Reserva'))
    
    class Meta:
        model= ReservaModel
        fields= ["id_cliente", "is_aluguel", "datahora_log", "id_espaco", "id_pacote_horas", "data_reserva", "hora_entrada", "hora_entrada_real", "hora_saida", "hora_saida_real", "hora_limpeza", "hora_limpeza_real", "preco_total"]

class AdvertenciaForm(forms.ModelForm):
    class Meta:
        model= AdvertenciasModel
        fields= ["comentario", "id_reserva", "id_funcionario"]

class ConvidadosForm(forms.ModelForm):
    class Meta:
        model= ConvidadosModel
        fields= ["id_reserva", "id_cliente", "email"]

class PagamentoForm(forms.ModelForm):
    class Meta:
        model= PagamentoModel
        fields= ["metodo", "cod_mercadopago", "status_pagamento", "id_equipamento"]

class EquipamentoreservaForm(forms.ModelForm):
    class Meta:
        model= EquipamentoreservaModel
        fields= ["id_reserva", "id_equipamento", "preco_locacao_equipamento", "id_pagamento"]

class FormTesteForm(forms.ModelForm):
    status_pagamento = forms.Select(
        attrs={'required': 'false'})
    class Meta:
        model= PagamentoModel
        fields= ["metodo", "cod_mercadopago", "status_pagamento"]

class FormTeste2Form(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label=_("Nome Completo"))
    numero_cartao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"0000.0000.0000.0000"}), label=_("Número do cartão"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    
    def clean_nome(self, *args, **kwargs):
        n = self.cleaned_data.get('nome')
        if n.replace(' ', '').isalpha():
            return self.cleaned_data.get('nome')
        else:
            h.raise_error(_('Não pode ter número no nome'), 'invalidName')
    # class Meta:
    #     fields= ["nome"]


class FormPagamento(forms.Form):
    TIPOS_DOCUMENTOS = (('rg', _('RG')), ('cpf', _('CPF')))
    PARCELAS_CHOICES = ((1, _('À vista')), 
                        (2, _('2x parcelas')),
                        (3, _('3x parcelas')),
                        (4, _('4x parcelas')),
                        (5, _('5x parcelas')),
                        (6, _('6x parcelas')) )
    BANCO_CHOICES = (('bradesco', _('Bradesco')),
                     ('santander', _('Santander')),
                     ('bancodobrasil', _('Banco do Brasil')),
                     ('nubank', _('Nubank')),
                     ('itau', _('Itaú')),
                     ('inter', _('Inter')),)
    BANCO_CHOICES = ((None, _('Insira primeiro o seu cartão')),)
    # BANCO_CHOICES = ((None, _('Insira primeiro o seu cartão')))

    numero_cartao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"0000.0000.0000.0000", 'id': 'id_numero_cartao'}), label=_("Número do cartão"))
    # data_vencimento = forms.CharField(widget=forms.TextInput(
    #     attrs={'required': 'true', 'data-mask':"00/00"}), label=_("Data vencimento"))
    mes_vencimento = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00", 'id': 'id_mes_vencimento'}), label=_("Mês vencimento"))
    ano_vencimento = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00", 'id': 'id_ano_vencimento'}), label=_("Ano vencimento"))
    nome_cartao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_nome_cartao'}), label=_("Nome descrito no cartão"))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_email'}), label=_("E-mail"))
    codigo_seguranca = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000", 'id': 'id_codigo_seguranca'}), label=_("Código de segurança")) 
    # parcelas = forms.IntegerField(widget=forms.NumberInput(
    #     attrs={'required': 'true', 'maxlength':"5", 'id': 'id_parcelas'}), label=_("Parcelas: "))
    parcelas = forms.CharField(widget=forms.Select(choices=PARCELAS_CHOICES,
        attrs={'required': 'true', 'id': 'id_parcelas'}), label=_("Parcelas"))
    tipo_documento = forms.CharField(widget=forms.Select(choices=TIPOS_DOCUMENTOS,
        attrs={'required': 'true', 'id': 'id_tipo_documento'}), label=_("Tipo do documento"))
    numero_documento = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_numero_documento'}), label=_("Número do documento"))
    banco = forms.CharField(widget=forms.Select(choices=BANCO_CHOICES,
        attrs={'required': 'true', 'id': 'id_banco'}), label=_("Banco/Bandeira"))
    # banco = forms.CharField(widget=forms.TextInput(
    #     attrs={'required': 'true', 'id': 'id_banco'}), label=_("Banco"))
    
    
    
    

    def clean_numero_cartao(self, *args, **kwargs):
        numero_cartao = self.cleaned_data.get('numero_cartao')
        valido = card_verifier.verify_card_number(numero_cartao)
        if valido:
            return numero_cartao
        else:
            h.raise_error(_('Insira um número de cartão válido'), 'invalidCardNumber')
    
    # def clean_data_vencimento(self, *args, **kwargs):
    #     data = self.cleaned_data.get('data_vencimento')
    #     erro = date_verifier.validate_expire_date(data)
    #     if not erro:
    #         return data
    #     else:
    #         h.raise_error(erro, 'invalidDate')

    def clean_mes_vencimento(self, *args, **kwargs):
        data = self.cleaned_data.get('mes_vencimento')
        erro = date_verifier.validate_expire_month(data)
        if not erro:
            return data
        else:
            h.raise_error(erro, 'invalidDate')
    
    def clean_ano_vencimento(self, *args, **kwargs):
        data = self.cleaned_data.get('ano_vencimento')
        erro = date_verifier.validate_expire_year(data)
        if not erro:
            return data
        else:
            h.raise_error(erro, 'invalidDate')

    def clean_nome_cartao(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("nome_cartao"), "nome")
        
        
    


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
            'is_active': True,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
                'link' : request.get_full_path()
            }
            context['link'] = context['link'].split('/')[1] + '/reset/'
            context['link'] = f"{context['protocol']}://{context['domain']}/{context['link']}{context['uid']}/{context['token']}"
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )

class MateriaisForm(forms.Form):
    nome_material = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label=_("Material"))
    valor_material = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label=_("Valor"))
    unidades_disponiveis = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label=_("Unidades disponíveis"))
    
   