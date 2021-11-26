from sys import stderr
from django.contrib.auth.models import Group, User

import common.views_util as h
import main.databases as d
from cria_coworking.models import Administrador
from domains.models import Domain
import cadastro


def configura_banco_e_dominio_materiais(data):
    nomedb = h.gera_nome_banco(data['nome'])
    data['database'] = nomedb
    d.create_database(nomedb)
    domain = Domain.objects.get(id=int(data['domain']))
    domain.isActive = 1
    domain.save()
    return data


def escreveNaTabelaMateriais(json, pessoa=False, administrador=True):
    nome_material = json.get('nome_material')
    valor_material = json['valor_material']
    descricao_material = json['descricao_material']
    unidades_disponiveis = json['unidades_disponiveis']

    # Salva na tabela materiais
    if administrador:
        return User.objects.create_material(username=cpf_cnpj, password=senha, email=email, first_name=first_name,
                                            last_name=last_name, is_superuser=True, is_staff=True)
    return User.objects.create_material(username=cpf_cnpj, password=senha,
                                        email=email, first_name=first_name, last_name=last_name)


def getDataNascimentoCliente(request):
    try:
        dataNascimento = request.POST['data_nascimento']
    except:
        dataNascimento = None
    return dataNascimento


def getDicionarioMateriaisForm(request):
    # JSON que formata os dados da request para o formulário corretamente
    data = {}

    fields = ["nome_material", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]

    for field in fields:
        data[field] = request.POST[field]
    return data


def writeMateriais(formMateriais, data):
    user = escreveNaTabelaMateriais(json=data, pessoa=False)

    cliente = formCliente.save(commit=False)  # Pega os dados do cliente
    cliente.user = user  # linka o usuário criado com o cliente
    cliente.save()  # Salva na tabela cliente
