from django import forms
from custom_templates.models import InstanceConfig
from django.utils.translation import gettext as _

# class FormPagamento(forms.Form):
#     cnpj = forms.CharField(widget=forms.TextInput(
#         attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label=_("CNPJ"))
#     email = forms.EmailField(widget=forms.EmailInput(
#         attrs={'required': 'true', 'maxlength':"70"}))
#     telefone = forms.CharField(widget=forms.TextInput(
#         attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
#     cep = forms.CharField(widget=forms.TextInput(
#         attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'id_administrador_cep'}))
#     logradouro = forms.CharField(widget=forms.TextInput(
#         attrs={'required': 'true', 'id': 'id_administrador_logradouro'}))
#     numero = forms.IntegerField(widget=forms.TextInput(
#         attrs={'required': 'true', 'maxlength':"5", 'id': 'id_administrador_numero'}))
#     bairro = forms.CharField(widget=forms.TextInput(
#         attrs={'required': 'true', 'id': 'id_administrador_bairro'}))
#     estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
#         attrs={'required': 'true', 'id': 'id_administrador_estado'}))
#     cidade = forms.CharField(widget=forms.TextInput(
#         attrs={'required': 'true', 'id': 'id_administrador_cidade'}))


class FormInstanceConfig(forms.ModelForm):
    showing_company_name = forms.CharField(label=_("Nome de exibição"))
    paleta1 = forms.CharField(label=_("Cor 1"), widget=forms.TextInput(attrs={'type': 'color'}))
    paleta2 = forms.CharField(label=_("Cor 2"), widget=forms.TextInput(attrs={'type': 'color'}))
    paleta3 = forms.CharField(label=_("Cor 3"), widget=forms.TextInput(attrs={'type': 'color'}))
    color_palette = forms.CharField(label=_("Paleta de cor"), required=False,
                                    widget=forms.TextInput(attrs={'type': 'hidden'}))
    client_logo = forms.ImageField(required=True)
    
    class Meta:
        model = InstanceConfig
        fields = ["paleta1", "paleta2", "paleta3", "color_palette", "showing_company_name", "client_logo"]
