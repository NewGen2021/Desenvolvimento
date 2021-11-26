from logging import warning
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import cria_coworking, sys
from django.shortcuts import render, redirect, resolve_url
import common.views_util as h
from cria_coworking.forms import CustomPasswordResetForm, RegistrarAdministradorForm, \
    RegistrarAdministradorInfosPessoaisForm
from domains.models import Domain
from cria_coworking.models import Administrador
from cria_coworking.services import getDicionarioAdministradorForm
from main.databases import create_database
import common.views_manager as m
import gere_coworking.services.cadastro as b_cadastro
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetView
from django.contrib.auth.decorators import login_required


@m.verificador(cria_coworking=True)
def index(request, context):
    # context = {'turl': h.get_url_without_langcode(request)}
    context['is_index'] = True
    dominio_id = Domain.objects.using('default').filter(domain=request.domain['domain'])[0].id
    try:
        database = Administrador.objects.using('default').get(domain=dominio_id)
    except ObjectDoesNotExist:
        database = 'default'
    return render(request, 'cria/index.html', context)


@m.verificador(cria_coworking=True)
def assinatura(request, context):
    return render(request, 'cria/assinatura.html', context)


@m.verificador(cria_coworking=True)
@login_required
def gerenciar_plano(request, context):
    context['Administrador'] = Administrador.objects.get(cnpj=request.user)
    return render(request, 'cria/gerenciar_plano.html', context)


@m.verificador(cria_coworking=True)
def registrarAdministradorOld(request, context):
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request, is_administrador=True)
        data['cnpj'] = h.retiraSimbolosString(data['cnpj'])

        administrador = RegistrarAdministradorForm(data)

        if administrador.is_valid():
            data = b_cadastro.configura_banco_e_dominio(data)
            b_cadastro.writeAdministrador(administrador, data)
            return redirect('index')

        context['administradorForm'] = administrador
    else:
        context['administradorForm'] = RegistrarAdministradorForm()
        context['administradorForm'].fields["domain"].queryset = Domain.objects.filter(isActive=0)

    return render(request, 'cria/regAdministrator.html', context)


@m.verificador(cria_coworking=True)
def registrarAdministrador(request, context):
    if request.method == "POST":
        data = getDicionarioAdministradorForm(request)
        data['cnpj'] = h.retiraSimbolosString(data['cnpj'])

        administrador = RegistrarAdministradorInfosPessoaisForm(data)

        if administrador.is_valid():
            b_cadastro.writeAdministrador(administrador, data)
            return redirect('index_cria')

        context['administradorForm'] = administrador
    else:
        context['administradorForm'] = RegistrarAdministradorInfosPessoaisForm()

    return render(request, 'cria/regAdministrator.html', context)


@m.verificador(cria_coworking=True)
def loginNewGen(request, context):
    if request.method == 'GET':
        return render(request, 'cria/login.html', context)

    user = h.autenticar(request)
    if user:
        login(request, user)
        return redirect('index_cria')
        # if h.isAdministrator(request):
        #     return redirect('index_cria')
        # context['grupo'] = h.getGrupoDoUsuario(request)
        # return render(request, 'cria/index.html', context)

    form = AuthenticationForm(data=request.POST)
    context['form'] = form
    context['mensagem_de_erro'] = h.getFormMensagemErro(form)

    return render(request, 'cria/login.html', context)

class CustomPasswordResetView(PasswordResetView):
    pass

class CustomPasswordResetDoneView(PasswordResetDoneView):
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordResetForm

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        context['login_newgen'] = 'login.html'
        context['login_system'] = 'loginSystem.html'
        context['isNewgen'] = True
        return context


