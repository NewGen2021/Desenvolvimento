from django.test import SimpleTestCase
from django.urls import reverse, resolve, reverse_lazy
import sys
import gere_coworking.views as gcv  # gere coworking view
import cria_coworking.views as ccv  # cria coworking view


class TestUrls_gere_coworking(SimpleTestCase):
	def __init__(self, methodName: str = ...) -> None:
		super().__init__(methodName=methodName)
		self.app = 'gere_coworking'
		self.urlconf = 'gere_coworking.urls'

	def test_list_url_index(self):
		url = reverse('index', urlconf=self.urlconf)
		self.assertEquals(resolve(url).func, gcv.index)

	def test_list_url_escolher_cadastro(self):
		url = reverse('escolherCadastro', urlconf=self.urlconf)
		self.assertEquals(resolve(url).func, gcv.escolherCadastro)

	def test_list_url_login_user(self):
		url = reverse('loginUser', urlconf=self.urlconf)
		self.assertEquals(resolve(url).func, gcv.loginUser)

	def test_list_url_login_system(self):
		url = reverse('loginSystem', urlconf=self.urlconf)
		self.assertEquals(resolve(url).func, gcv.loginSystem)

	def test_list_url_login_novo(self):
		url = reverse('loginNovo', urlconf=self.urlconf)
		self.assertEquals(resolve(url).func, gcv.loginNovo)

	def test_list_url_registrar_usuario(self):
		url = reverse('registrarUsuario', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.registrarUsuario)

	def test_list_url_registrar_funcionario(self):
		url = reverse('registrarFuncionario', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.registrarFuncionario)

	def test_list_url_registrar_admin(self):
		url = reverse('registrarAdmin', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.registrarAdministrador)

	def test_list_url_agendamento(self):
		url = reverse('agendamento', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.agendamento)

	def test_list_url_reserva(self):
		url = reverse('reserva', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.reserva)

	def test_list_url_listar_reservas(self):
		url = reverse('listarReservas', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.listarReservas)

	def test_list_url_listar_reservas_index(self):
		url = reverse('listarReservasIndex', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.listarReservasIndex)

	def test_list_url_menu_admin(self):
		url = reverse('menuAdmin', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.menuAdmin)

	def test_list_url_customizacao(self):
		url = reverse('customizacao', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.customizacao)

	def test_list_url_em_producao(self):
		url = reverse('emProducao', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.emProducao)

	def test_list_url_base_html(self):
		url = reverse('baseHtml', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.base_html)

	def test_list_url_teste(self):
		url = reverse('teste', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.teste)


class TestUrls_cria_coworking(SimpleTestCase):
	def __init__(self, methodName: str = ...) -> None:
		super().__init__(methodName=methodName)
		self.urlconf = 'cria_coworking.urls'

	def test_list_url_index(self):
		url = reverse('index', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ccv.index)

	def test_list_url_registrarAdmin(self):
		url = reverse('registrarAdmin', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ccv.registrarAdministrador)
