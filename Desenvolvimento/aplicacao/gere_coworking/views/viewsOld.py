from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User, UserManager
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, UsernameField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user
from django.template.context_processors import csrf

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
    return render(request, 'cliente_final/apresentacao/home.html', {'grupo': grupo})

def loginUser(request):
    return render(request, 'old/loginUser.html')

def loginSystem(request):
    context={'lng': request.session.get('lng', 'pt')}
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

    context = {}
    if request.method == "POST":

        usuario = LoginForm(data=request.POST)

        user = h.autenticar(request)
        if user:
            login(request, user)
            if h.isAdministrator(request):
                return redirect('menuAdmin')
            context['grupo'] = h.getGrupoDoUsuario(request)
            return render(request, 'cliente_final/apresentacao/index.html', context)

        context['loginForm'] = usuario
    else:
        context['loginForm'] = LoginForm

    return render(request, 'cliente_final/cadastro_e_login/loginNovo.html', context)

def escolherCadastro(request):
    contexto = {}
    return render(request, 'cliente_final/cadastro_e_login/escolherCadastro.html', contexto)




def registrarUsuario(request):
    context = {}
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
    # if request.method == "POST":
    #     funcionario = FuncionariosForm(request.POST)
    #     if funcionario.is_valid():
    #         user = b_cadastro.escreveNaTabelaUser(json=request.POST, pessoa=True)
    #         funcionario.save()  # Salva na tabela funcionario
    #         b_cadastro.configuraGrupoUsuario(user, tipo='funcionario')
    #         return redirect('loginSystem')
    #     messages.error(request, 'Formulário inválido!')
    #     return redirect('funcionarios/regEmployee.html')
    # else:
    #     form = FuncionariosForm
    #     return render(request, 'funcionarios/regEmployee.html', {'form': form})

    context = {}
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
    # if request.method == "POST":
    #     funcionario = RegistrarAdministradorForm(request.POST)
    #     if funcionario.is_valid():
    #         user = b_cadastro.escreveNaTabelaUser(json=request.POST, pessoa=False, administrador=True)
    #         funcionario.save()  # Salva na tabela funcionario
    #         b_cadastro.configuraGrupoUsuario(user, tipo='administrador')
    #         return redirect('loginSystem')
    #     messages.error(request, 'Formulário inválido!')
    #     return redirect('registrarUsuario')
    # else:
    #     form = RegistrarAdministradorForm
    #     return render(request, 'gerenciamentoCoworking/regAdministrator.html', {'form': form})
    context = {}
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request, is_administrador=True)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        administrador = RegistrarAdministradorForm(data)

        if administrador.is_valid():
            b_cadastro.writeFuncionario(administrador, data)
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
    }
    return render(request, 'cliente_final/agendamento/reserva2Calendario.html', context)

def assinatura(request):
    return render(request, 'cliente_final/apresentacao/assinatura.html')

def index(request):
    return render(request, 'cliente_final/apresentacao/index.html')

def reserva(request):
    return render(request, 'cliente_final/agendamento/reserva1EscolherEspaco.html')

def listarReservas(request):
    reservas = ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username)
    context = {
        'reservas': reservas
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
        return render(request, 'administrador/menuAdmin.html')
    else:
        return render(request, 'cliente_final/apresentacao/index.html', {'admInvalid': True})

def customizacao(request):
    return render(request, 'administrador/customizacao.html')

def emProducao(request):
    return render(request, 'gerenciamentoCoworking/emProducao.html')

def reset_password(request):
    return render(request, 'cadastro_e_login/reset_password.html')

