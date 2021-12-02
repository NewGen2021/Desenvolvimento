"""
    * Métodos focados na verificação de datas
    * Favor manter em ordem alfabética
"""

import datetime
from django.utils.translation import gettext as _

minimo = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
maximo = datetime.datetime.strptime('2100-12-31', '%Y-%m-%d')
idade_minima = 10
DIFERENCIA_ANO_MAXIMO_VENCIMENTO = 20


def datetime_format(date, format):
    try:
        return datetime.datetime.strptime(date, format)
    except ValueError:
        return False


def format_date(date):
    if isinstance(date, str):
        formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']
        for format in formats:
            formatted_date = datetime_format(date, format)
            if formatted_date:
                return formatted_date
        raise ValueError(
            f'{date} não está em um formato válido.')
    if isinstance(date, datetime.datetime):
        return date
    if isinstance(date, datetime.date):
        return datetime.datetime.combine(date, datetime.datetime.min.time())
    raise TypeError(f'Não foi possível formatar {type(date)} de {date}. Tipos suportados: datetime.datetime, str.')


def get_minimum_birth_date_year():
    present = datetime.datetime.now()
    present = datetime.datetime.now()
    return present.year - idade_minima - 1


def validate_birthday_date(date):
    date = format_date(date)
    present = datetime.datetime.now()
    minimum_age = datetime.timedelta(days=365*idade_minima)
    if (present - date) < minimum_age:
        return False
    return validate_date(date)


def validate_date(date):
    tested_date = format_date(date)
    if tested_date < minimo:
        return False
    if tested_date > maximo:
        return False
    return True

def validate_expire_date(date):
    mes, ano = date.split('/')
    mes = int(mes)
    ano = int(ano)
    ano_atual = int(str(datetime.datetime.today().year)[2:])
    if mes < 1 or mes > 12:
        return _('Insira uma data válida no formato mm/yy, ex: 07/25')
    if ano < ano_atual or ano > ano_atual + DIFERENCIA_ANO_MAXIMO_VENCIMENTO:
        return _(f'Insira um ano válido no formato yy até {DIFERENCIA_ANO_MAXIMO_VENCIMENTO} anos. Ex: 07/27')
    return False

def validate_expire_month(month):
    mes = int(month)
    if mes < 1 or mes > 12:
        return _('Insira uma data válida no formato mm/yy, ex: 07/25')
    return False

def validate_expire_year(year):
    ano = int(year)
    ano_atual = int(str(datetime.datetime.today().year)[2:])
    if ano < ano_atual or ano > ano_atual + DIFERENCIA_ANO_MAXIMO_VENCIMENTO:
        return _(f'Insira um ano válido no formato yy até {DIFERENCIA_ANO_MAXIMO_VENCIMENTO} anos. Ex: 07/27')
    return False