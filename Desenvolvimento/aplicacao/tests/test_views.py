from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from django.urls import reverse
from domains.models import Domain
from threading import local
from django.test.client import RequestFactory
import json, sys
from functools import wraps
from django.conf import settings
from importlib import reload
from django.urls import clear_url_caches
from tests.conf_tests import selecionar_app, reload_urlconf
from gere_coworking.models import ClienteModel, FuncionariosModel
from gere_coworking.services.cadastro import configuraGrupoUsuario
import datetime


tests_local = local()
class TestViews_gere_coworking(TestCase):
    # multi_db = True
    def setUp(self) -> None:
        self.client = Client()
        Group.objects.create(name='administrador')
        Group.objects.create(name='clienteEmpresa')
        Group.objects.create(name='clientePessoa')
        Group.objects.create(name='funcionario')
        # self.clientePessoa = User.objects.create_user(
        #     username='112.207.848-00',
        #     email='nicolashalvesalmeida@armyspy.com', 
        #     first_name='Nicolas',
        #     last_name='Almeida', 
        #     is_superuser=False, 
        #     is_staff=False)
        # self.clientePessoa.set_password('newgen123')
        # self.clientePessoa.save()
        # configuraGrupoUsuario(self.clientePessoa, tipo='pessoa')
        # tests_local.current_app = 'gere_coworking'
        # reload_urlconf()
        # response = Client().post(reverse('registrarUsuario'), {
        #     'form-selecionado': 'pessoaFisica',
        #     'nome': 'Tiago Ribeiro',
        #     'senha': 'newgen123',
        #     'cpf_cnpj': '309.940.155-26',
        #     'data_nascimento': '12/09/1986',
        #     'genero': 'M',
        #     'email': 'tiagocavalcantiribeiro@gmail.com',
        #     'telefone': '11977866159',
        #     'cep': '04611-060',
        #     'logradouro': 'Rua Alberto Gebara',
        #     'numero': '1604',
        #     'bairro': 'Parque Colonial',
        #     'cidade': 'São Paulo',
        #     'estado': 'SP'
        #     })
        # self.user1_cliente = ClienteModel.objects.get(cpf_cnpj='30994015526')

    @selecionar_app(app='gere_coworking')
    def test_index_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/index.html')
    
    # LOGAR!
    @selecionar_app(app='gere_coworking')
    def test_home_GET(self):
        # response = self.client.get(reverse('home'))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/home.html')
        pass
    
    @selecionar_app(app='gere_coworking')
    def test_login_user_GET(self):
        response = self.client.get(reverse('loginUser'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'old/loginUser.html')
    
    @selecionar_app(app='gere_coworking')
    def test_login_system_GET(self):
        response = self.client.get(reverse('loginSystem'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/cadastro_e_login/loginSystem.html')
    
    @selecionar_app(app='gere_coworking')
    def test_login_novo_GET(self):
        response = self.client.get(reverse('loginNovo'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/cadastro_e_login/loginNovo.html')
    
    @selecionar_app(app='gere_coworking')
    def test_escolher_cadastro_GET(self):
        response = self.client.get(reverse('escolherCadastro'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/cadastro_e_login/escolherCadastro.html')
    
    @selecionar_app(app='gere_coworking')
    def test_registrar_usuario_GET(self):
        response = self.client.get(reverse('registrarUsuario'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/cadastro_e_login/regUsers.html')
    
    @selecionar_app(app='gere_coworking')
    def test_registrar_funcionario_GET(self):
        response = self.client.get(reverse('registrarFuncionario'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/funcionario/regEmployee.html')
    
    @selecionar_app(app='gere_coworking')
    def test_index_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/index.html')
    
    @selecionar_app(app='gere_coworking')
    def test_registrar_administrador_GET(self):
        response = self.client.get(reverse('registrarAdmin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cria/regAdministrator.html')
    
    # LOGAR!
    @selecionar_app(app='gere_coworking')
    def test_agendamento_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/index.html')
    
    # DEPRECATED!
    @selecionar_app(app='gere_coworking')
    def test_assinatura_GET(self):
        # response = self.client.get(reverse('index'))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/assinatura.html')
        pass
    
    @selecionar_app(app='gere_coworking')
    def test_reserva_GET(self):
        response = self.client.get(reverse('reserva'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/agendamento/reserva1EscolherEspaco.html')
    
    # LOGAR!
    @selecionar_app(app='gere_coworking')
    def test_listar_reservas_GET(self):
        # response = self.client.get(reverse('listarReservas'))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'gere/template1/cliente/agendamento/listarReservas.html')
        pass
    
    # LOGAR!
    @selecionar_app(app='gere_coworking')
    def test_listar_reservas_index_GET(self):
        # response = self.client.get(reverse('listarReservasIndex'))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'gere/template1/cliente/agendamento/listarReservasIndex.html')
        pass
    
    # LOGAR!
    @selecionar_app(app='gere_coworking')
    def test_menu_admin_GET(self):
        # response = self.client.get(reverse('menuAdmin'))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/index.html')
        pass
    
    @selecionar_app(app='gere_coworking')
    def test_customizacao_GET(self):
        response = self.client.get(reverse('customizacao'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/adm/customizacao.html')
    
    @selecionar_app(app='gere_coworking')
    def test_em_producao_GET(self):
        response = self.client.get(reverse('emProducao'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'erros/emProducao.html')
    
    @selecionar_app(app='gere_coworking')
    def test_base_GET(self):
        response = self.client.get(reverse('baseHtml'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/base.html')
    
    @selecionar_app(app='gere_coworking')
    def test_teste_GET(self):
        response = self.client.get(reverse('teste'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'gere/template1/cliente/apresentacao/teste.html')
    
    @selecionar_app(app='gere_coworking')
    def test_password_reset_GET(self):
        # response = self.client.get(reverse('password_reset'))
        # self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'gere/template1/cliente/cadastro_e_login/password_reset.html')
        pass
    
    def test_registrar_usuario_POST_adicionar_novo_cliente_pessoa(self):
        response = self.client.post(reverse('registrarUsuario'), {
            'form-selecionado': 'pessoaFisica',
            'nome': 'Douglas Rodrigues',
            'senha': 'newgen123',
            'cpf_cnpj': '783.729.355-05',
            'data_nascimento': '19/01/1986',
            'genero': 'M',
            'email': 'douglassouzarodrigues@rhyta.com',
            'telefone': '11977866159',
            'cep': '91920-270',
            'logradouro': 'Rua da Fraternidade',
            'numero': '1604',
            'bairro': 'Cavalhada',
            'cidade': 'Porto Alegre',
            'estado': 'RS'
            })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(ClienteModel.objects.get(cpf_cnpj='78372935505').nome, 'Douglas Rodrigues')
    
    def test_registrar_usuario_POST_adicionar_novo_cliente_empresa(self):
        response = self.client.post(reverse('registrarUsuario'), {
            'form-selecionado': 'pessoaJuridica',
            'nome': 'Telework',
            'senha': 'newgen123',
            'cpf_cnpj': '28.704.761/0001-43',
            'email': 'telework@jourrapide.com',
            'telefone': '11977866159',
            'cep': '03335-085',
            'logradouro': 'Praça Fernando Zago',
            'numero': '1874',
            'bairro': 'Vila Regente Feijó',
            'cidade': 'São Paulo',
            'estado': 'SP'
            })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(ClienteModel.objects.get(cpf_cnpj='28704761000143').nome, 'Telework')

    def test_registrar_funcionario_POST_adicionar_novo_funcionario(self):
        response = self.client.post(reverse('registrarFuncionario'), {
            'nome': 'Marina Rocha',
            'senha': 'newgen123',
            'cpf_cnpj': '368.910.764-47',
            'data_nascimento': '31/03/1999',
            'genero': 'F',
            'email': 'marinasouzarocha@jourrapide.com',
            'telefone': '11977866159',
            'cep': '91920-270',
            'logradouro': 'Praça Fernando Zago',
            'numero': '1874',
            'bairro': 'Vila Regente Feijó',
            'cidade': 'São Paulo',
            'estado': 'SP'
            })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(FuncionariosModel.objects.get(cpf_cnpj='36891076447').nome, 'Marina Rocha')

    # def test_login_system_POST_logar_usuario(self):
    #     user = User.objects.create_user(
    #         username='112.207.848-00',
    #         password='a', 
    #         email='nicolashalvesalmeida@armyspy.com', 
    #         first_name='Nicolas',
    #         last_name='Almeida', 
    #         is_superuser=False, 
    #         is_staff=False)
    #     configuraGrupoUsuario(user, tipo='pessoa')
    #     user.set_password('newgen123')
    #     user.save()
    #     response = self.client.post(reverse('loginSystem'), {
    #         'username': '11220784800',
    #         'password': 'newgen123'
    #     })
        
    #     self.assertEquals(response.status_code, 302)
        

class TestViews_cria_coworking(TestCase):
    # multi_db = True
    def setUp(self) -> None:
        self.client = Client()

    @selecionar_app(app='cria_coworking')
    def test_index_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cria/index.html')
    
    @selecionar_app(app='cria_coworking')
    def test_registrar_administrador_GET(self):
        response = self.client.get(reverse('registrarAdmin'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cria/regAdministrator.html')

# class TestViews_cria_coworking(TestCase):
#     # multi_db = True
#     def __init__(self, methodName: str = ...) -> None:
#         super().__init__(methodName=methodName)
#         self.urlconf = 'cria_coworking.urls'
    
#     def test_index_GET(self):
#         tests_local.current_app = 'cria_coworking'
#         client = Client(capp='cria_coworking')
#         response = client.get(reverse('index', urlconf='cria_coworking.urls'))
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'cria/index.html')

# class SimpleTest(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()

#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('/customer/details')

#         # Test my_view() as if it were deployed at /customer/details
#         response = my_view(request)
#         self.assertEqual(response.status_code, 200)