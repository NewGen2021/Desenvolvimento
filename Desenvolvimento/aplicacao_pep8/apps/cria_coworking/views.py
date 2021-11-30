from logging import warning
from threading import Thread
from custom_templates.models import InstanceConfig
from custom_templates.services import instantiate_custom_config, instantiate_template_index, \
    mount_all_customs
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import common.selectors as selector
from django.views.decorators.csrf import csrf_protect
import cria_coworking, sys
from django.shortcuts import render, redirect, resolve_url
import common.views_util as h
from cria_coworking.forms import CustomPasswordResetForm, RegistrarAdministradorForm, \
    RegistrarAdministradorInfosPessoaisForm, CriaCoworkingFormPagamento, \
    CriarCoworkingForm, CriarContaInstanciaForm
from domains.models import Domain
from cria_coworking.models import Administrador
from cria_coworking.services import getDicionarioAdministradorForm, \
    redirect_if_already_has, criar_instancia_nova
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
from django.core.mail import send_mail


@m.verificador(cria_coworking=True)
def index(request, context):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        send_mail(
            subject,
            message,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

    context['is_index'] = True
    dominio_id = Domain.objects.using('default').filter(domain=request.domain['domain'])[0].id
    try:
        database = Administrador.objects.using('default').get(domain=dominio_id)
    except ObjectDoesNotExist:
        database = 'default'
    return render(request, 'cria/index.html', context)


@login_required
@m.verificador(cria_coworking=True)
def assinatura(request, context):
    if response := redirect_if_already_has(request):
        return response
    return render(request, 'cria/assinatura.html', context)


@login_required
@m.verificador(cria_coworking=True)
def pagar_plano(request, context):
    if request.method == "POST":
        form = CriaCoworkingFormPagamento(request.POST)
        mensagem_de_erro = request.POST['mensagem_de_erro']
        if mensagem_de_erro == '' or mensagem_de_erro == 'none':
            return redirect('registrarCoworking')
        else:
            context['form'] = form
    else:
        if response := redirect_if_already_has(request):
            return response
        context['form'] = CriaCoworkingFormPagamento()
    context['adm'] = selector.get_administrador_logado_in_cria(request)
    return render(request, 'cria/pagamento.html', context)


@m.verificador(cria_coworking=True)
@login_required
def gerenciar_plano(request, context):
    context['Administrador'] = Administrador.objects.get(cnpj=request.user)
    try:
        context['Instancia'] = InstanceConfig.objects.get(client_id=context['Administrador'])
    except InstanceConfig.DoesNotExist:
        context['Instancia'] = None
    adm = selector.get_administrador_logado_in_cria(request)
    criando = adm.database == None and request.GET.get('aviso_inicial') and adm.domain != None
    context['avisar_estado_criacao'] = True if criando else False
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
            usuario = b_cadastro.writeAdministradorInCriaCoworking(administrador, data)
            user = authenticate(request, username=data['cnpj'], password=data['senha'])
            if not user:
                print('USUARIO')
                print(usuario)
                print(usuario.username)
                print(usuario.password)
                # return redirect('index_cria')
            login(request, user)
            return redirect('assinatura')

        context['administradorForm'] = administrador
    else:
        context['administradorForm'] = RegistrarAdministradorInfosPessoaisForm()

    return render(request, 'cria/regAdministrator.html', context)


@m.verificador(cria_coworking=True)
@login_required
def registrarCoworking(request, context):
    if request.method == "POST":
        instancia = CriarCoworkingForm(request.POST, request.FILES)
        if instancia.is_valid():
            request.session['POST'] = request.POST
            adm = selector.get_administrador_logado_in_cria(request)
            button = request.session['POST']['button_design'] if request.session['POST']['button_design'] else 'btn-primary'
            
            instantiate_custom_config(cliente = adm,
                                      nome=request.session['POST']['showing_company_name'],
                                      cor1=request.session['POST']['paleta1'],
                                      cor2=request.session['POST']['paleta2'],
                                      cor3=request.session['POST']['paleta3'],
                                      button=button,
                                      client_logo=request.FILES['client_logo'])
            return redirect('registrarContaNaInstancia')
        context['form'] = instancia
    else:
        context['form'] = CriarCoworkingForm()
        context['form'].fields["paleta1"].queryset = '#428bca'
        context['form'].fields["paleta2"].queryset = '#f1f1f1'
        context['form'].fields["paleta3"].queryset = '#5c768d'

    return render(request, 'cria/regCoworking.html', context)


@m.verificador(cria_coworking=True)
@login_required
def registrarContaNaInstancia(request, context):
    if not request.session.get('POST'):
        return redirect('registrarCoworking')
    adm = selector.get_administrador_logado_in_cria(request)
    if request.method == "POST":
        conta = CriarContaInstanciaForm(request.POST)
        if conta.is_valid():
            domain = request.session['POST']['domain']
            data = {'nome': request.session['POST']['showing_company_name'],
                    'domain': domain,
                    'senha': request.POST['senha1'],
                    'email': adm.email,
                    'cnpj': adm.cnpj}
            adm.domain = Domain.objects.get(id=domain)
            adm.save()
            criar_instancia_nova(data, adm, context)
            return redirect(reverse('gerenciar_plano')+"?aviso_inicial=true")
        context['form'] = conta
    else:
        context['form'] = CriarContaInstanciaForm(initial={'cnpj': adm.cnpj})
        # context['form'].fields["cnpj"].queryset = Domain.objects.filter(isActive=0)
    return render(request, 'cria/regContaInstancia.html', context)


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


