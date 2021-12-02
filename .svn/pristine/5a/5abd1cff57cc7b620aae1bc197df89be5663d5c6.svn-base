"""
    * Métodos focados na verificação de campos de texto (e.g. nome e endereço)
    * Favor manter em ordem alfabética
"""
from django.utils.translation import gettext as _


def get_address_errors(address):
    address = address.replace(' ', '')
    contains_invalid_expression = randomness_analysis(address)
    if not address.isalnum():
        return _('Não são permitidos símbolos neste campo.')
    if not address.isalpha():
        return _('Não são permitidos números neste campo. Coloque o número do endereço no seu respectivo campo.')
    if contains_invalid_expression:
        return _('Confira se alguma letra está duplicada.')


def get_address_number_errors(address_number):
    address_number = str(address_number).strip()
    if len(address_number) > 5:
        return _('Números de endereço só podem ser até 5 caracteres.')
    if not address_number.isalnum():
        return _('Não são permitidos símbolos ou espaços no número do endereço.')
    if not address_number.isdigit():
        before_last_char = address_number[:-1]
        if not before_last_char.isdigit():
            return _('Colocar complementos no formato 111a, 111b.')
    return ''


def get_name_errors(name, pessoa=True):
    name = name.strip()
    if not name.replace(' ', '').isalpha() and pessoa == True:
        return _('Certifique-se que o nome só contém letras. Números e símbolos não são permitidos.')
    if len(name) < 5:
        return _('Nome curto demais, colocar pelo menos 5 caracteres.')
    lista = name.split(' ')
    if len(lista) == 1 and pessoa:
        return _('Por favor coloque nome completo.')
    contains_invalid_expression = randomness_analysis(name)
    if contains_invalid_expression:
        return _('Confira se alguma letra está duplicada.')
    return ''


def randomness_analysis(name):
    random_container = ['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'lll', 'mmm',
                        'nnn', 'ooo', 'ppp', 'qqq', 'rrr', 'sss', 'ttt', 'uuu', 'vvv', 'www', 'xxx', 'yyy', 'zzz', ]
    for expression in random_container:
        if name.replace(' ', '').__contains__(expression):
            return True
    return False
