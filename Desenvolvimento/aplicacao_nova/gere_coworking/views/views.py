from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User, UserManager
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, UsernameField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth import get_user
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate

from django.template.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect

from crispy_forms.utils import render_crispy_form

from newgen.settings import BASE_DIR
from gere_coworking.forms.forms import *
import gere_coworking.views.views_helper as h    # 'h' de "helping"
import gere_coworking.views.businessLayer.cadastro as b_cadastro   # 'b' de 'business"
import gere_coworking.views.businessLayer.reserva as b_reserva   # 'b' de 'business"

import os
import datetime, sys

#print("Comentários do console", file=sys.stderr)

# Create your views here.
def home(request):
    grupo = h.getGrupoDoUsuario(request)
    
    context = {'turl': h.get_url_without_langcode(request), 'grupo': grupo}
    return render(request, 'cliente_final/apresentacao/home.html', context)

def loginUser(request):
    context = {'turl': h.get_url_without_langcode(request)}
    return render(request, 'old/loginUser.html', context)

def loginSystem(request):
    context={'turl': h.get_url_without_langcode(request)}
    if request.method == 'GET':
        return render(request, 'cliente_final/cadastro_e_login/loginSystem.html', context)
    
    user = h.autenticar(request)
    if user:
        login(request, user)
        if h.isAdministrator(request):
            return redirect('menuAdmin')
        context['grupo'] = h.getGrupoDoUsuario(request)
        return render(request, 'cliente_final/apresentacao/index.html', context)


    form = AuthenticationForm(data=request.POST)
    context['form'] = form
    context['mensagem_de_erro'] = h.getFormMensagemErro(form)

    return render(request, 'cliente_final/cadastro_e_login/loginSystem.html', context)

def loginNovo(request):

    context={'turl': h.get_url_without_langcode(request)}
    if request.method == 'POST':
        user = h.autenticar(request)
        print('----------------------- CARALHO1', file=sys.stderr)
        if user:
            login(request, user)
            if h.isAdministrator(request):
                return redirect('menuAdmin')
            context['grupo'] = h.getGrupoDoUsuario(request)
            print('----------------------- CARALHO2', file=sys.stderr)
            return render(request, 'cliente_final/apresentacao/index.html', context)

        context['form'] = AuthenticationForm(data=request.POST)
        context['mensagem_de_erro'] = h.getLoginErrors(request)
    else:
        context['form'] = AuthenticationForm()
        context['mensagem_de_erro'] = ''

    print('----------------------- CARALHO3', file=sys.stderr)

    return render(request, 'cliente_final/cadastro_e_login/loginNovo.html', context)

    

def escolherCadastro(request):
    #if request.method == 'POST':
       
    #  print(request)
    context = {'turl': h.get_url_without_langcode(request)}
    return render(request, 'cliente_final/cadastro_e_login/escolherCadastro.html', context)




def registrarUsuario(request):
    context={'turl': h.get_url_without_langcode(request)}
    if request.method == "POST":
        data = b_cadastro.getDicionarioClienteForm(request)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        cliente = ClientePessoaForm(data)
        isPerson = True
        formSelecionado = b_cadastro.getFormSelecionado(request)
        if formSelecionado == "pessoaJuridica":
            cliente = ClienteEmpresaForm(data)
            isPerson = False
        
        if cliente.is_valid():
            b_cadastro.writeCliente(cliente, data, isPerson)
            return redirect('loginSystem')

        if formSelecionado == "pessoaFisica":
            context['pessoaForm'] = cliente
            context['empresaForm'] = ClienteEmpresaForm
        else:
            context['pessoaForm'] = ClientePessoaForm
            context['empresaForm'] = cliente
        context['selecionado'] = formSelecionado

    else:
        context['pessoaForm'] = ClientePessoaForm
        context['empresaForm'] = ClienteEmpresaForm
        context['selecionado'] = "pessoaFisica"

    return render(request, 'cliente_final/cadastro_e_login/regUsers.html', context)
    
def registrarFuncionario(request):
    
    context={'turl': h.get_url_without_langcode(request)}
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        funcionario = FuncionariosForm(data)

        if funcionario.is_valid():
            b_cadastro.writeFuncionario(funcionario, data)
            return redirect('loginSystem')

        context['funcionarioForm'] = funcionario
    else:
        context['funcionarioForm'] = FuncionariosForm

    return render(request, 'funcionarios/regEmployee.html', context)

    

def registrarAdministrador(request):
    
    context={'turl': h.get_url_without_langcode(request)}
    
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request, is_administrador=True)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        administrador = RegistrarAdministradorForm(data)

        if administrador.is_valid():
            b_cadastro.writeFuncionario(administrador, data, administrador=True)
            return redirect('loginSystem')

        context['administradorForm'] = administrador
    else:
        context['administradorForm'] = RegistrarAdministradorForm

    return render(request, 'gerenciamentoCoworking/regAdministrator.html', context)

@login_required
def agendamento(request, id_tipo_espaco):
    # Chama as reservas já feitas com uma data futura a hoje de um determinado tipo de espaço

    compartilhado = b_reserva.isCompartilhado(id_tipo_espaco)
    event_list = b_reserva.getEventoReservasCliente(request, id_tipo_espaco)

    reservas = ReservaModel.objects.get_reservas_atuais(id_tipo_espaco = id_tipo_espaco)
    dateDicts = b_reserva.getDicionarioReservas(id_tipo_espaco)
    
    '''Importante'''
    vagas_max = 2

    print('------------- DATE DICTS', file=sys.stderr)
    print(dateDicts, file=sys.stderr)

    event_list = b_reserva.getEventoReservasLotadas(dateDicts, vagas_max, event_list)
    
    # print('------------- EVENT LIST', file=sys.stderr)
    # print(event_list, file=sys.stderr)

    hasErrors = False
    error = None
    
    if request.method == 'POST':
        dicionario = b_reserva.getForm(request, id_tipo_espaco)

        
        form = ReservaForm(dicionario)
        if form.is_valid():
            hasErrors, error = b_reserva.getFormErrors(dicionario, event_list)
            # Salva o formulário se ele não contiver erros
            if not hasErrors:
                form.save()
                context = {
                    'token': True,
                    'reservas': reservas,
                }
                return redirect('listarReservas')
        else:
            error = 'Formulário inválido: '
            for k, v in form.errors.as_json.items():
                error += f'Campo {k} : {v}'

    else:
        form = ReservaForm

    context = {
        # 'reservas': reservas,
        'eventos': event_list,
        'form': form,
        'hasErrors': hasErrors,
        'error': error,
        'compartilhado': compartilhado,
        'turl': h.get_url_without_langcode(request),
    }
    return render(request, 'cliente_final/agendamento/reserva2Calendario.html', context)

def assinatura(request):
    
    context={'turl': h.get_url_without_langcode(request)}
    return render(request, 'cliente_final/apresentacao/assinatura.html', context)

#@csrf_protect
def index(request):
    #request.session['lng'] = 'pt'
    if request.method == "POST":
        request.session['lng'] = 'en'
    ### POST NO INDEX SOMENTE PRA SETAR O COOKIE DE IDIOMA!
    
    context={'turl': h.get_url_without_langcode(request)}
    return render(request, 'cliente_final/apresentacao/index.html', context)

def reserva(request):
    if request.method == "POST":
        request.session['lng'] = 'en'
    context = {'turl': h.get_url_without_langcode(request)}
    return render(request, 'cliente_final/agendamento/reserva1EscolherEspaco.html', context)

def listarReservas(request):
    reservas = ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username)
    context = {
        'reservas': reservas,
        'turl': h.get_url_without_langcode(request)
    }
    return render(request, 'cliente_final/agendamento/listarReservas.html', context)

def listarReservasIndex(request):
    reservas = ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username)
    eventos = b_reserva.getEventoReservasCliente(request, 0)
    context = {
        'reservas': reservas,
        'eventos': eventos,
    }
    return render(request, 'cliente_final/agendamento/listarReservasIndex.html', context)

def menuAdmin(request):
    if h.isAdministrator(request):
        context={'turl': h.get_url_without_langcode(request)}
        return render(request, 'administrador/menuAdmin.html', context)
    else:
        context={'turl': h.get_url_without_langcode(request), 'admInvalid': True}
        return render(request, 'cliente_final/apresentacao/index.html', context)

def customizacao(request):
    context={'turl': h.get_url_without_langcode(request)}
    return render(request, 'administrador/customizacao.html', context)

def emProducao(request):
    context={'turl': h.get_url_without_langcode(request)}
    return render(request, 'gerenciamentoCoworking/emProducao.html', context)


def base_html(request):
    return render(request, 'base.html')

def teste(request):
    context = {
        'mundo': _('mundo'),
        'turl': h.get_url_without_langcode(request),
    }
    return render(request, 'cliente_final/apresentacao/teste.html', context)

def translate(language):
	cur_language = get_language()
	try:
		activate(language)
		text = _('WORLD')
	finally:
		activate(cur_language)
	return text
