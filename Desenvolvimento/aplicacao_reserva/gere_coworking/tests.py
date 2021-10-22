from aplicacao.newgenapp.models import Espacos
from django.test import TestCase
import unittest
from newgenapp.models import Tipoespaco
from newgenapp.models import Pagamento
from newgenapp.models import Espacos
from newgenapp.models import Equipamentos

# Create your tests here.
class TipoespacoTestCase(unittest.TestCase):
    def descriptionTest(self):
        self.id_tipoespaco = Tipoespaco.objects.create(tipo="Mesa compartilhada", descricao="Mais de um assento")
        self.nome = Tipoespaco.objects.create(tipo="Sala de apresentação", descricao="Com retroprojetor")

class PagamentoTestCase(unittest.TestCase):
    def validationTest(self):
        self.metodo = Pagamento.objects.create(tipo="Boleto bancário", parcelas="Nao")

class PagamentoTestCase(unittest.TestCase):
    def validationTest(self):
        self.fatura = Pagamento.objects.create(tipo="Boleto bancário", parcelas="Nao")

class EspacosTestCase(unittest.TestCase):
    def confimacaoTest(self):
        self.espaco = Espacos.objects.create(nome="Sala 01", descricao="Andar terreo", preco="R$ 75,00")

class EquipamentosTestCase(unittest.TestCase):
    def dadosTest(self):
        self.dados = Equipamentos.objects.create(nome="Telefone sem fio", status="Danificado", preco="R$ 175,00")

