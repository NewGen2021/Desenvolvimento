'''
    * Classe para pegar dados de um determinado cep
    * Favor manter em ordem alfabética
'''

import requests
import ast

class Cep:

    # Construtor
    def __init__(self, cep):
        self.cep = self.format_cep(cep)
        html_doc = requests.get(f"http://cep.republicavirtual.com.br/web_cep.php?cep={cep}&formato=jsonp").content
        self.dicionario = dicionario = ast.literal_eval(html_doc.decode('ascii'))
        self.resultado = dicionario['resultado']
        self.resultado_txt = dicionario['resultado_txt']
        self.uf = dicionario['uf']
        self.cidade = dicionario['cidade']
        self.bairro = dicionario['bairro']
        self.tipo_logradouro = dicionario['tipo_logradouro']
        self.logradouro = dicionario['logradouro']

    @staticmethod
    def format_cep(cep):
        return cep.replace('-', '').replace('.', '').replace(' ', '')

    def is_cep_valid(self):
        if len(self.cep) != 8:
            return False
        if self.cep.isdigit() is False:
            return False
        if self.resultado == '0':
            return False
        return True


def is_cep_valid(cep):
    return Cep(cep).is_cep_valid()
