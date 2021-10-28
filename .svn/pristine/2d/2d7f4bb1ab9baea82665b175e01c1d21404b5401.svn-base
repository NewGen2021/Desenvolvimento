from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Widget

from crispy_forms.helper import FormHelper

from gere_coworking.models.models import *
from gere_coworking.models.models_choice import *
from gere_coworking.forms.verifiers.cpfVerifier import *
from gere_coworking.forms.verifiers.cnpjVerifier import *
from gere_coworking.forms.verifiers.phoneVerifier import *
from gere_coworking.forms.verifiers.dateVerifier import *
from gere_coworking.forms.verifiers.cepVerifier import *

from gere_coworking.forms import forms_helper as h
from gere_coworking.forms.verifiers.cnpjVerifier import formatCNPJ
from gere_coworking.forms.verifiers.cpfVerifier import formatCpf

import sys

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label="CPF/CNPJ")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true'}), label='Senha')
    
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
        print('--------------------- USERNAME 2222222222 ')
        print(username, file=sys.stderr)
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            return username
        except User.DoesNotExist:
            h.raise_error('Usuário com o CPF informado não existe!', 'not_exists')

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
            user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise h.raise_error('Senha incorreta, tente novamente.', 'incorrect')
            return password
        except User.DoesNotExist:
            h.raise_error('Usuário com o CPF informado não existe!', 'not_exists')


class RegistrarAdministradorForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"70"}), label="Razão social")
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label="CNPJ")
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
        attrs={'required': 'true', 'maxlength':"70"}), label="Nome Completo")
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000.000.000-00"}), label="CPF", max_length=11)
    data_nascimento = forms.DateField(widget=forms.TextInput(
        attrs={'data-mask': '00/00/0000', 'required': 'true'}), label="Data de Nascimento")
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
        attrs={'required': 'true'}), label="Razão Social")
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label="CNPJ")
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
    """ nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="Nome Completo")
    genero = forms.Select(
        attrs={'required': 'false'})
    logradouro = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    estado = forms.Select(
        attrs={'required': 'true'})
    cidade = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={'required': 'true'}))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))

    class Meta:
        model= FuncionariosModel
        fields= ["nome", "senha", "cpf_cnpj", "data_nascimento", "genero", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"] """
    # FIELDS
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"70"}), label="Nome Completo")
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000.000.000-00"}), label="CPF", max_length=11)
    data_nascimento = forms.DateField(widget=forms.TextInput(
        attrs={'data-mask': '00/00/0000', 'required': 'true'}), label="Data de Nascimento")
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
    class Meta:
        model= TipoespacoModel
        fields= ["descricao", "nome", "ultima_alteracao", "data_ultima_alteracao", "tempo_limpeza", "preco"]

class EquipamentosForm(forms.ModelForm):
    class Meta:
        model= EquipamentosModel
        fields= ["tipo", "descrição", "preco", "ultima_alteracao", "status_equipamento", "data_ultima_alteracao"]

class PacoteHorasForm(forms.ModelForm):
    class Meta:
        model= PacotehorasModel
        fields= ["id_cliente", "qtd_horas", "id_empresa", "status_pacotehoras"]

class EspacosForm(forms.ModelForm):
    class Meta:
        model= EspacosModel
        fields= ["id_tipo_espaco", "ultima_alteracao", "status_espaco", "data_ultima_alteracao"]

class ReservaForm(forms.ModelForm):
    data_reserva = forms.DateField(widget=forms.TextInput(attrs={'data-mask':'00/00/0000', 'required':'true'}), label='Data de Reserva')
    
    class Meta:
        model= ReservaModel
        fields= ["id_cliente", "id_pagamento", "datahora_log", "id_espaco", "id_pacote_horas", "data_reserva", "hora_entrada", "hora_entrada_real", "hora_saida", "hora_saida_real", "hora_limpeza", "hora_limpeza_real", "preco_total"]

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
        fields= ["metodo", "cod_mercadopago", "status_pagamento", "datahora_log", "id_reserva", "id_equipamento"]

class EquipamentoreservaForm(forms.ModelForm):
    class Meta:
        model= EquipamentoreservaModel
        fields= ["id_reserva", "id_equipamento", "preco_locacao_equipamento", "id_pagamento"]