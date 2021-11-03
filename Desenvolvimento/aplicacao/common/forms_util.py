from common.form_fields_verifiers.cpfVerifier import *
from common.form_fields_verifiers.cnpjVerifier import *
from common.form_fields_verifiers.phoneVerifier import *
from common.form_fields_verifiers import dateVerifier
from common.form_fields_verifiers.cepVerifier import *
from common.form_fields_verifiers.textVerifiers import *
from typing import Callable
from gere_coworking.selectors import is_cliente_duplicated
from cria_coworking.selectors import is_adm_duplicated

from django import forms
from django.utils.translation import gettext as _

import sys


def null_function() -> bool:
    return False

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
        return validate_adm_cnpj(var)
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
        raise_error(f"{_('Data de nascimento inválida! Escolha entre 1900 e ')}{dateVerifier.get_minimum_birth_date_year()}.", 'invalid')
    return birthday_date


def validate_cep(cep):
    if not is_cep_valid(cep):
        raise_error(_("CEP não existe."), code='invalid')
    return cep


def validate_adm_cnpj(cnpj: str):
    if not isCNPJValid(cnpj):
        raise_error(_("CNPJ inválido"), code='invalid')
    if is_adm_duplicated(cnpj):
       raise_error(_("CNPJ já registrado! Insira outro por favor."), code='duplicated')
    return cnpj


def validate_cnpj(cnpj: str, isClient: bool=True):
    if not isCNPJValid(cnpj):
        raise_error(_("CNPJ inválido"), code='invalid')
    if is_cliente_duplicated(cnpj, tipo_pessoa= "cliente" if isClient else "funcionario"):
       raise_error(_("CNPJ já registrado! Insira outro por favor."), code='duplicated')
    return cnpj


def validate_cpf(cpf: str, asEmployee:bool=False):
    if not isCpfValid(cpf):
        raise_error(_("CPF inválido"), "invalid")

    if is_cliente_duplicated(cpf, tipo_pessoa= "cliente" if not asEmployee else "funcionario"):
        raise_error(_("CPF já registrado! Insira outro por favor."), "duplicated")
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
        raise_error(_("Telefone inválido!"), code='invalid')
    return telephone

