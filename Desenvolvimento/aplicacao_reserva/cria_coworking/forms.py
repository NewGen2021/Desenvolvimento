from django import forms

from cria_coworking.models import Administrador, availableDomains
from gere_coworking.forms import forms_helper as h
from gere_coworking.models.models_choice import *
from django.utils.translation import gettext as _

# class RegistrarAdministradorForm(forms.Form):
#     nome = forms.CharField(widget=forms.TextInput(
#             attrs={'required': 'true', 'id': 'id_nome_gerente'}))
#     """ senha = forms.CharField(widget=forms.TextInput(
#             attrs={'required': 'true', 'id': 'id_senha_gerente'})) """

#     # class Meta:
#     #     fields= ["cidade", ""]

class RegistrarAdministradorForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"70"}), label=_("Razão social"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength':"40"}))
    cnpj = forms.CharField(widget=forms.TextInput(
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
        model= Administrador
        fields= ["nome", "senha", "domain", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    
    # VERIFIERS
    def clean_cnpj(self, *args, **kwargs):
        return h.validate(self.cleaned_data.get("cnpj"), "cnpj_administrador")
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
