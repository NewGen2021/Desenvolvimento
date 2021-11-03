'''
    * Métodos simples usados na view
    * Favor manter em ordem alfabética
'''

from gere_coworking.forms.verifiers.cnpjVerifier import formatCNPJ
from gere_coworking.forms.verifiers.cpfVerifier import formatCpf
from gere_coworking.forms import forms_helper as h
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import sys

def autenticar(request):
    username = format_cpf_cnpj(request.POST['username'])
    password = request.POST['password']
    return authenticate(request, username=username, password=password)

def capitalizaNome(string):
    palavras = string.strip().split(' ')
    for contador, palavra in enumerate(palavras):
        palavras[contador] = palavra.capitalize()
    nome = ' '.join(palavras)
    return nome

def format_cpf_cnpj(cpf_cnpj):
    cpf_cnpj = formatCNPJ(cpf_cnpj)
    cpf_cnpj = formatCpf(cpf_cnpj)
    return cpf_cnpj

def getGrupoDoUsuario(request):
    l = request.user.groups.values_list('name',flat = True) # QuerySet Object
    l_as_list = list(l)
    grupo = str(l_as_list[0])
    return grupo

def getFormMensagemErro(Form):
    erros = Form.errors.get_json_data(escape_html=False)
    if len(erros) == 0:
        return ''
    elif len(erros) == 1:
        mensagem = ''
        for value in erros.values():
            mensagem = value[0]["message"]
        return mensagem
    else:
        mensagens = []
        for value in erros.values():
            mensagens.append(value[0]["message"])
        return mensagens

def getLoginErrors(request):
    username = request.POST['username']
    password = request.POST['password']
    try:
        user = User.objects.get(username=username)
        user_cache = authenticate(request, username=username, password=password)
        if user_cache is None:
            return 'Senha incorreta, tente novamente.'
        return password
    except User.DoesNotExist:
        return 'Usuário com o CPF informado não existe!'

def isAdministrator(request):
    grupo = getGrupoDoUsuario(request)
    if grupo == 'administrador':
        return True
    return False

# Confere se o tempo 2 está dentro do tempo 1
def isInPeriod(time1_start, time1_end, time2_start, time2_end):
    return True or False

def retiraSimbolosString(string):
    return string.replace('-', '').replace('.', '').replace('/', '')

