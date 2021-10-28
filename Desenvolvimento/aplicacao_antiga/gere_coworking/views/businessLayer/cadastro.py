'''
    * Métodos usados especificamente na funcionalidade de cadastro e login no sistema
    * Favor manter em ordem alfabética
'''

from sys import stderr
from django.contrib.auth.models import Group, User

import gere_coworking.views.views_helper as h

def configuraGrupoUsuario(usuario, tipo):
    if tipo == 'pessoa':
        my_group = Group.objects.get(name='clientePessoa')        
        my_group.user_set.add(usuario)
    elif tipo == 'empresa':
        my_group = Group.objects.get(name='clienteEmpresa')        
        my_group.user_set.add(usuario)
    elif tipo == 'funcionario':
        my_group = Group.objects.get(name='funcionario')        
        my_group.user_set.add(usuario)
    elif tipo == 'administrador':
        my_group = Group.objects.get(name='administrador')        
        my_group.user_set.add(usuario)
    else:
        raise ValueError('Função configuraGrupoUsuario não reconhece o tipo ' + tipo)


def escreveNaTabelaUser(json, pessoa=True, administrador=False):
    cpf_cnpj = json['cpf_cnpj']
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

    # Salva na tabela user
    if administrador:
        return User.objects.create_user(username=cpf_cnpj, password=senha, email=email, first_name=first_name,
         last_name=last_name, is_superuser=True, is_staff=True)
    return User.objects.create_user(username=cpf_cnpj, password=senha,
    email=email, first_name=first_name, last_name=last_name)

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
    else:
        fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    print('------------------------- AAAAAAA', file=stderr)
    print(request.POST , file=stderr)
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
    formCliente.save()  # Salva na tabela cliente

def writeFuncionario(formFuncionario, data, administrador=False):
    if administrador:
        user = escreveNaTabelaUser(json=data, pessoa=False, administrador=True)
        configuraGrupoUsuario(user, tipo='administrador')
    else:
        user = escreveNaTabelaUser(json=data, pessoa=True)
        configuraGrupoUsuario(user, tipo='funcionario')
    formFuncionario.save()  # Salva na tabela cliente