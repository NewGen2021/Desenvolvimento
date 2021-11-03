import sys
from django import forms
import unicodedata

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from cria_coworking.models import Administrador, availableDomains
from gere_coworking.forms import forms_helper as h
from gere_coworking.models.models_choice import *
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
            context ['link'] = context ['link'].split('/')[1] + '/reset/'
            context ['link'] = f"{context ['protocol']}://{context ['domain']}/{context ['link']}{context ['uid']}/{context ['token']}"
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )

