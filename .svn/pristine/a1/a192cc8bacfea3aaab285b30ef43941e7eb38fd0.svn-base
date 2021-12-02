"""
    * Métodos usados especificamente na funcionalidade de cadastro e login no sistema
    * Favor manter em ordem alfabética
"""

from sys import stderr
from django.contrib.auth.models import Group, User

import common.views_util as h
import newgen.databases as d
from cria_coworking.models import Administrador
from domains.models import Domain

def configura_banco_e_dominio(data: dict) -> dict:
    nomedb = h.gera_nome_banco(data['nome'])
    data['database'] = nomedb
    d.create_database(nomedb)
    domain = Domain.objects.get(id=int(data['domain']))
    domain.isActive = 1
    domain.save()
    return data

def configuraGrupoUsuario(usuario, tipo, banco: str=None):
    if tipo == 'pessoa':
        name='clientePessoa'
    elif tipo == 'empresa':
        name='clienteEmpresa'
    elif tipo == 'funcionario':
        name='funcionario'
    elif tipo == 'administrador':
        name='administrador'
    else:
        raise ValueError('Função configuraGrupoUsuario não reconhece o tipo "' + tipo + '"')
    if banco:
        my_group = Group.objects.using(banco).get(name=name)
    else:
        my_group = Group.objects.get(name=name)
    my_group.user_set.add(usuario)


def escreveNaTabelaUser(json, pessoa=True, administrador=False, banco: str=None) -> User:
    cpf_cnpj = json.get('cnpj') if administrador else json.get('cpf_cnpj')
    email = json['email']
    senha = json['senha']

    # Formatação do nome
    nome = json['nome']
    if pessoa:
        nome = nome.split(' ')
        first_name = h.capitalizaNome(nome[0])
        nome.pop(0)
        last_name = ' '.join(nome)
        last_name = h.capitalizaNome(last_name)
    else:
        first_name = h.capitalizaNome(json['nome'])
        last_name = ''
        
    # new_user = User()
    # new_user.username = cpf_cnpj
    # new_user.password = senha
    # new_user.email = email
    # new_user.first_name = first_name
    # new_user.last_name = last_name
    
    # Salva na tabela user
    if administrador:
        # new_user.is_superuser = True
        # new_user.is_staff = True
        if banco is not None:
            return User.objects.db_manager(banco).create_user(username=cpf_cnpj, 
            password=senha, email=email, first_name=first_name, last_name=last_name, 
            is_superuser=True, is_staff=True)
        return User.objects.create_user(username=cpf_cnpj, 
            password=senha, email=email, first_name=first_name, last_name=last_name, 
            is_superuser=True, is_staff=True)
    if banco is not None:
        return User.objects.db_manager(banco).create_user(username=cpf_cnpj, password=senha,
        email=email, first_name=first_name, last_name=last_name)
    return User.objects.create_user(username=cpf_cnpj, password=senha,
        email=email, first_name=first_name, last_name=last_name)
    # if banco is not None:
    #     new_user.save(using=banco)
    # else:
    #     new_user.save()
    # print('paoksdpokas')
    # print(new_user)
    return new_user

def getDataNascimentoCliente(request):
    try:
        dataNascimento = request.POST['data_nascimento']
    except:
        dataNascimento = None
    return dataNascimento

def getDicionarioClienteForm(request):
    # JSON que formata os dados da request para o formulário corretamente
    data = {}

    # Confere pela data de nascimento se é um form de empresa ou cliente
    dataNascimento = getDataNascimentoCliente(request)
    if dataNascimento is not None:
        fields = ["nome", "senha", "cpf_cnpj", "data_nascimento", "genero", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]
    else:
        fields = ["nome", "senha", "cpf_cnpj", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]
    for field in fields:
        data[field] = request.POST[field]
    return data

def getDicionarioFuncionarioForm(request, is_administrador=False):
    data = {}

    if not is_administrador:
        fields = ["nome", "senha", "data_nascimento", "cpf_cnpj", "genero", "email", "telefone", "cep", "logradouro", "numero", "bairro", "cidade", "estado"]
       # fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    else:
        fields = ["nome", "senha", "domain", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    for field in fields:
        data[field] = request.POST[field]
    return data

def getFormSelecionado(request):
    options = ["pessoaFisica", "pessoaJuridica"]
    return request.POST['form-selecionado']

def writeCliente(formCliente, data, isPerson):
    if isPerson:
        user = escreveNaTabelaUser(json=data, pessoa=True)
        configuraGrupoUsuario(user, tipo='pessoa')
    else:
        user = escreveNaTabelaUser(json=data, pessoa=False)
        configuraGrupoUsuario(user, tipo='empresa')
    cliente = formCliente.save(commit=False)  # Pega os dados do cliente
    cliente.user = user  # linka o usuário criado com o cliente
    cliente.save()  # Salva na tabela cliente

def writeFuncionario(formFuncionario, data):
    user = escreveNaTabelaUser(json=data, pessoa=True)
    configuraGrupoUsuario(user, tipo='funcionario')
    funcionario = formFuncionario.save(commit=False)  # Salva na tabela cliente
    funcionario.user = user
    funcionario.save()

def writeAdministradorInCriaCoworking(formAdministrador, data) -> User:
    user = escreveNaTabelaUser(json=data, pessoa=False, administrador=True)
    configuraGrupoUsuario(user, tipo='administrador')    
    # adm = Administrador.objects.get(cnpj=data['cnpj'])
    # adm.database = data['database']
    # adm.save()
    formAdministrador.save()
    return user

def writeAdministradorInGereCoworking(data, banco) -> User:
    user = escreveNaTabelaUser(json=data, pessoa=False, administrador=True, banco=banco)
    configuraGrupoUsuario(user, tipo='administrador')    
    # adm = Administrador.objects.get(cnpj=data['cnpj'])
    # adm.database = data['database']
    # adm.save()
    return user