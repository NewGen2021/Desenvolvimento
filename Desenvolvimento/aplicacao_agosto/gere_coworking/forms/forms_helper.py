from gere_coworking.forms.verifiers.cpfVerifier import *
from gere_coworking.forms.verifiers.cnpjVerifier import *
from gere_coworking.forms.verifiers.phoneVerifier import *
from gere_coworking.forms.verifiers import dateVerifier
from gere_coworking.forms.verifiers.cepVerifier import *
from gere_coworking.forms.verifiers.textVerifiers import *

from gere_coworking.models.models import *

from django import forms

import sys

def raise_error(message, code):
    raise forms.ValidationError(message=message, code=code)

def validate(var, tipo):
    tipo = tipo.lower()
    if tipo == 'cpf':
        return validate_cpf(var)
    if tipo == 'cpf_funcionario':
        return validate_cpf(var, asEmployee=True)
    if tipo == 'cnpj':
        return validate_cnpj(var)
    if tipo == 'cnpj_administrador':
        return validate_cnpj(var, isClient=False)
    if tipo == 'telefone':
        return validate_telephone(var)
    if tipo == 'data_nascimento':
        return validate_birthday_date(var)
    if tipo == 'cep':
        return validate_cep(var)
    if tipo == 'nome':
        return validate_name(var)
    if tipo == 'nome_empresa':
        return validate_name(var, pessoa=False)
    if tipo == 'numero_endereco':
        return validate_address_number(var)
    if tipo == 'endereco':
        return validate_address(var)
    opcoes = ['cpf', 'cpf_funcionario', 'cnpj', 'telefone', 'data_nascimento', 'cep', 'nome', 'numero_endereco', 'endereco', 'nome_empresa']
    raise ReferenceError('Não foi possível localizar o tipo ' + tipo + '\nAs tipos válidos são: ' + opcoes)


def validate_address(address):
    error_message = get_address_errors(address)
    if error_message:
        raise_error(error_message, code='invalid')
    return address


def validate_address_number(address_number):
    error_message = get_address_number_errors(address_number)
    if error_message:
        raise_error(error_message, code='invalid')
    return address_number


def validate_birthday_date(birthday_date):
    if not dateVerifier.validate_birthday_date(birthday_date):
        raise_error(f"Data de nascimento inválida! Escolha entre 1900 e {dateVerifier.get_minimum_birth_date_year()}.", 'invalid')
    return birthday_date


def validate_cep(cep):
    if not is_cep_valid(cep):
        raise_error(f"CEP não existe.", code='invalid')
    return cep


def validate_cnpj(cnpj, isClient=True):
    if not isCNPJValid(cnpj):
        raise_error("CNPJ inválido", code='invalid')
    if ClienteModel.objects.is_duplicated(cnpj, tipo_pessoa= "cliente" if isClient else "funcionario"):
       raise_error("CNPJ já registrado! Insira outro por favor.", code='duplicated')
    return cnpj


def validate_cpf(cpf, asEmployee=False):
    if not isCpfValid(cpf):
        raise_error("CPF inválido", "invalid")

    if ClienteModel.objects.is_duplicated(cpf, tipo_pessoa= "cliente" if not asEmployee else "funcionario"):
        raise_error("CPF já registrado! Insira outro por favor.", "duplicated")
    return cpf
    # print('-------------- A', file=sys.stderr)
    # if FuncionariosModel.objects.is_duplicated(cpf, tipo_pessoa="funcionario"):
    #     print('-------------- B', file=sys.stderr)
    #     raise_error("CPF já registrado! Insira outro por favor.", "duplicated")
    # return cpf


def validate_name(name, pessoa=True):
    error_message = get_name_errors(name, pessoa=pessoa)
    if error_message:
        raise_error(error_message, code='invalid')
    return name


def validate_telephone(telephone):
    if not is_telephone_valid(telephone):
        raise_error("Telefone inválido!", code='invalid')
    return telephone



