import sys
from django import forms
from common.views_util import retiraSimbolosString
import unicodedata
from domains.models import Domain
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from cria_coworking.models import Administrador, availableDomains
from common import forms_util as h
from common.models_choices import *
from django.utils.translation import gettext as _
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes

UserModel = get_user_model()


# class RegistrarAdministradorForm(forms.Form):
#     nome = forms.CharField(widget=forms.TextInput(
#             attrs={'required': 'true', 'id': 'id_nome_gerente'}))
#     """ senha = forms.CharField(widget=forms.TextInput(
#             attrs={'required': 'true', 'id': 'id_senha_gerente'})) """

#     # class Meta:
#     #     fields= ["cidade", ""]

class RegistrarAdministradorForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength': "70"}), label=_("Razão social"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '8', 'maxlength': "40",
                'data-toggle':"tooltip", 'data-placement':"top", 'title':"A senha deve ter no máximo 8 caracteres"}))
    cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "00.000.000/0000-00"}), label=_("CNPJ"))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true', 'maxlength': "70"}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "00000-000", 'id': 'id_administrador_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_logradouro'}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength': "5", 'id': 'id_administrador_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_bairro'}))
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
                                                 attrs={'required': 'true', 'id': 'id_administrador_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_cidade'}))

    # def __init__(self, *args, **kwargs):
    #     super(RegistrarAdministradorForm, self).__init__(*args, **kwargs)
    #     self.fields = ["nome", "senha", "domain", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    #     # if exclude_fields != []:
    #     #     for field in exclude_fields:
    #     #         self.fields.remove(field)
    def __init__(self, *args, **kwargs):
        exclude_fields: list = [] if not 'exclude_fields' in kwargs else kwargs.pop('exclude_fields')

        super().__init__(*args, **kwargs)
        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field)

        # for field in self.fields.items():
        # self.fields['nome'] = Administrador.objects.using('default').all()

    class Meta:
        model = Administrador
        fields = ["nome", "senha", "domain", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro",
                  "estado", "cidade"]

    # VERIFIERS
    def clean_cnpj(self):
        cnpj = retiraSimbolosString(self.cleaned_data.get("cnpj"))
        return h.validate(cnpj, "cnpj_allow_duplicate")

    def clean_telefone(self):
        return h.validate(self.cleaned_data.get("telefone"), "telefone")

    # def clean_cep(self):
    #     return h.validate(self.cleaned_data.get("cep"), "cep")

    # def clean_nome(self):
    #     return h.validate(self.cleaned_data.get("nome"), "nome_empresa")

    def clean_numero(self):
        return h.validate(self.cleaned_data.get("numero"), "numero_endereco")

    # def clean_logradouro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("logradouro"), "endereco")
    # def clean_bairro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("bairro"), "endereco")
    def clean_cidade(self):
        return h.validate(self.cleaned_data.get("cidade"), "endereco")

class RegistrarAdministradorInfosPessoaisForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength': "70"}), label=_("Razão social"))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '8', 'maxlength': "40", 'id': 'input_senha',
                'data-toggle':"tooltip", 'data-placement':"top", 'title':_("A senha deve ter no mínimo 8 caracteres")}),
                label=_("Senha (mínimo 8 caracteres)"))
    cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "00.000.000/0000-00"}), label=_("CNPJ"))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true', 'maxlength': "70"}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "00000-000", 'id': 'id_administrador_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_logradouro'}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength': "5", 'id': 'id_administrador_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_bairro'}))
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS_ESTADOS,
                                                 attrs={'required': 'true', 'id': 'id_administrador_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_administrador_cidade'}))

    # def __init__(self, *args, **kwargs):
    #     super(RegistrarAdministradorForm, self).__init__(*args, **kwargs)
    #     self.fields = ["nome", "senha", "domain", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    #     # if exclude_fields != []:
    #     #     for field in exclude_fields:
    #     #         self.fields.remove(field)
    def __init__(self, *args, **kwargs):
        exclude_fields: list = [] if not 'exclude_fields' in kwargs else kwargs.pop('exclude_fields')

        super().__init__(*args, **kwargs)
        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field)

        # for field in self.fields.items():
        # self.fields['nome'] = Administrador.objects.using('default').all()

    class Meta:
        model = Administrador
        fields = ["nome", "senha", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]

    # VERIFIERS
    def clean_cnpj(self):
        return h.validate(self.cleaned_data.get("cnpj"), "cnpj_administrador")

    def clean_telefone(self):
        return h.validate(self.cleaned_data.get("telefone"), "telefone")

    # def clean_cep(self):
    #     return h.validate(self.cleaned_data.get("cep"), "cep")

    # def clean_nome(self):
    #     return h.validate(self.cleaned_data.get("nome"), "nome_empresa")
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Administrador.objects.filter(email=email).exists():
            raise forms.ValidationError(message=_("O e-mail informado já está sendo usado."), code='duplicated')
        return email
        
    def clean_numero(self):
        return h.validate(self.cleaned_data.get("numero"), "numero_endereco")

    # def clean_logradouro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("logradouro"), "endereco")
    # def clean_bairro(self, *args, **kwargs):
    #     return h.validate(self.cleaned_data.get("bairro"), "endereco")
    def clean_cidade(self):
        return h.validate(self.cleaned_data.get("cidade"), "endereco")


class CriaCoworkingFormPagamento(forms.Form):
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

    nome_cartao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_nome_cartao'}), label=_("Nome descrito no cartão"))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_email'}), label=_("E-mail"))
    tipo_documento = forms.CharField(widget=forms.Select(choices=TIPOS_DOCUMENTOS,
        attrs={'required': 'true', 'id': 'id_tipo_documento'}), label=_("Tipo do documento"))
    numero_documento = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_numero_documento'}), label=_("Número do documento"))
    parcelas = forms.CharField(widget=forms.Select(choices=PARCELAS_CHOICES,
        attrs={'required': 'true', 'id': 'id_parcelas'}), label=_("Parcelas"))
    numero_cartao = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"0000.0000.0000.0000", 'id': 'id_numero_cartao'}), label=_("Número do cartão"))
    # data_vencimento = forms.CharField(widget=forms.TextInput(
    #     attrs={'required': 'true', 'data-mask':"00/00"}), label=_("Data vencimento"))
    mes_vencimento = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00", 'id': 'id_mes_vencimento'}), label=_("Mês de vencimento"))
    ano_vencimento = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00", 'id': 'id_ano_vencimento'}), label=_("Ano de vencimento"))
    codigo_seguranca = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000", 'id': 'id_codigo_seguranca'}), label=_("Código de segurança")) 
    # parcelas = forms.IntegerField(widget=forms.NumberInput(
    #     attrs={'required': 'true', 'maxlength':"5", 'id': 'id_parcelas'}), label=_("Parcelas: "))
    banco = forms.CharField(widget=forms.Select(choices=BANCO_CHOICES,
        attrs={'required': 'true', 'id': 'id_banco'}), label=_("Banco/Bandeira"))
    # banco = forms.CharField(widget=forms.TextInput(
    #     attrs={'required': 'true', 'id': 'id_banco'}), label=_("Banco"))


def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()


class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    @staticmethod
    def send_mail(subject_template_name, email_template_name,
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

    @staticmethod
    def get_users(email):
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
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )


class CriarCoworkingForm(forms.Form):
    def get_domain_choices() -> tuple:
        dominios_disponiveis = Domain.objects.filter(isActive=0)
        
        lista_aux = []
        for dominio in dominios_disponiveis:
            lista_aux.append((dominio.id, dominio.domain))
        return tuple(lista_aux)
    DOMAIN_CHOICES = get_domain_choices()
    paleta1 = forms.CharField(label=_("Cor 1"), widget=forms.TextInput(
        attrs={'type': 'color', 'value': '#428bca', 'class':"tooltip-test", 'title':_('Cor de destaque')}))
    paleta2 = forms.CharField(label=_("Cor 2"), widget=forms.TextInput(
        attrs={'type': 'color', 'value': '#f1f1f1', 'class':"tooltip-test", 'title':_('Cor do fundo')}))
    paleta3 = forms.CharField(label=_("Cor 3"), widget=forms.TextInput(
        attrs={'type': 'color', 'value': '#5c768d', 'class':"tooltip-test", 'title':_('Cor do rodapé')}))
    color_palette = forms.CharField(label=_("Paleta de cor"), required=False,
                                    widget=forms.TextInput(attrs={'type': 'hidden'}))
    showing_company_name = forms.CharField(label=_("Nome de exibição"))
    client_logo = forms.ImageField(required=True, label=_("Logo da empresa"))
    domain = forms.IntegerField(widget=forms.Select(choices=DOMAIN_CHOICES), label=_("Domínios disponíveis"))
    
    class Meta:
        fields = ["paleta1", "paleta2", "paleta3", "color_palette", "domain", "showing_company_name", "client_logo"]

class CriarContaInstanciaForm(forms.Form):

    cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask': "00.000.000/0000-00"}), label=_("CNPJ"))
    senha1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength': "40"}), label=_("Senha"))
    senha2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6', 'maxlength': "40"}), label=_("Confirme a senha"))
    
    class Meta:
        fields = ["cnpj", "senha1", "senha2"]
    
    def clean_cnpj(self):
        return h.validate(self.cleaned_data.get("cnpj"), "cnpj_allow_duplicate")
    
    def clean_senha2(self):
        senha1 = self.cleaned_data.get("senha1")
        senha2 = self.cleaned_data.get("senha2")
        if senha1 != senha2:
            raise forms.ValidationError(message=_("As senhas precisam ser iguais."), code='invalid_duplicated')
        return senha2