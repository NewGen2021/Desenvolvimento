from django.test import SimpleTestCase
from django.urls import reverse, resolve, reverse_lazy
import sys
import gere_coworking.views as gcv  # gere coworking view
import cria_coworking.views as ccv  # cria coworking view
import custom_templates.views as ctv  # cria coworking view


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

	def test_list_url_pagamento_reserva(self):
		url = reverse('pagamento_reserva', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.form_pagamento)

	def test_list_url_reset_password(self):
		url = reverse('reset_password', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func.view_class, gcv.PasswordResetView)

	def test_list_url_password_reset_done(self):
		url = reverse('password_reset_done', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func.view_class, gcv.CustomPasswordResetDoneView)

	# def test_list_url_password_reset_confirm(self):
	# 	url = reverse('password_reset_confirm', urlconf=self.urlconf)
	# 	self.assertEquals(resolve(url, urlconf=self.urlconf).func.view_class, gcv.CustomPasswordResetConfirmView)

	def test_list_url_password_reset_complete(self):
		url = reverse('password_reset_complete', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func.view_class, gcv.CustomPasswordResetCompleteView)

	def test_list_url_qrcode_envio(self):
		url = reverse('qrcode_envio', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.gerar_qrcode)

	def test_list_url_finaliza_reserva(self):
		url = reverse('finaliza_reserva', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.finalizaReserva)
	
	def test_list_url_listar_espacos(self):
		url = reverse('listar_espacos', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.listar_espacos)

	def test_list_url_editar_tipo_espaco(self):
		url = reverse('editar_tipo_espaco', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.editar_tipo_espaco)

	def test_list_url_editar_espaco(self):
		url = reverse('editar_espaco', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.editar_espaco)

	def test_list_url_criar_tipo_espaco(self):
		url = reverse('criar_tipo_espaco', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.criar_tipo_espaco)

	def test_list_url_criar_espaco(self):
		url = reverse('criar_espaco', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.criar_espaco)

	def test_list_url_excluir_tipo_espaco(self):
		url = reverse('excluir_tipo_espaco', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.excluir_tipo_espaco)

	def test_list_url_excluir_espaco(self):
		url = reverse('excluir_espaco', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.excluir_espaco)

	def test_list_url_testarLayout(self):
		url = reverse('testarLayout', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.testarLayout)

	def test_list_url_testarLayout2(self):
		url = reverse('testarLayout2', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.testarLayout2)

	def test_list_url_render_view(self):
		url = reverse('render_view', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ctv.render_view)

	def test_list_url_teste_render(self):
		url = reverse('teste_render', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ctv.teste_render)

	def test_list_url_base_funcionario(self):
		url = reverse('base_funcionario', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.base_funcionario)

	def test_list_url_menuFunc(self):
		url = reverse('menuFunc', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.menuFunc)

	def test_list_url_leitor_qrcode(self):
		url = reverse('leitor_qrcode', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.leitor_qrcode)

	def test_list_url_testando_qrcode(self):
		url = reverse('testando_qrcode', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.testando_qrcode)

	def test_list_url_custom_personal_info(self):
		url = reverse('custom_personal_info', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ctv.custom_personal_info)

	def test_list_url_custom_cowork_info(self):
		url = reverse('custom_cowork_info', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ctv.custom_cowork_info)

	def test_list_url_custom_index(self):
		url = reverse('custom_index', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ctv.custom_index)

	def test_list_url_relatorio_advertencia(self):
		url = reverse('relatorio/advertencia', urlconf=self.urlconf, args=[1])
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.advertencia)

	def test_list_url_relatorio_view(self):
		url = reverse('relatorio_view/', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.tela_relatorio)
	
	def test_list_url_bootstrap(self):
		url = reverse('testar_bootstrap', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, gcv.testar_bootstrap)

#    path('comentarios', ComentarioList.as_view(), name="comentarios"),
#    path('relatorio_view/alugueis', AluguelList.as_view(), name='relatorios/aluguel'),
#    path('relatorio_view/reservas_geral', Todas_Resrvas.as_view(), name='relatorios_view/reservas_geral'),
#    path('relatorio/reservas', ReservaList.as_view(), name='relatorios/reservas'),
#    path('relatorio_view/pagamentos', PagamentoList.as_view(), name="relatorios/pagamentos"),
#    path('testar_bootstrap', testar_bootstrap, name='testar_bootstrap'),




class TestUrls_cria_coworking(SimpleTestCase):
	def __init__(self, methodName: str = ...) -> None:
		super().__init__(methodName=methodName)
		self.urlconf = 'cria_coworking.urls'

	def test_list_url_index(self):
		url = reverse('index_cria', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ccv.index)

	def test_list_url_registrarAdmin(self):
		url = reverse('registrarAdmin', urlconf=self.urlconf)
		self.assertEquals(resolve(url, urlconf=self.urlconf).func, ccv.registrarAdministrador)
