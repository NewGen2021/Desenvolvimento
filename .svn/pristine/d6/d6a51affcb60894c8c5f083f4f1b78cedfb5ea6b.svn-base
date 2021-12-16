from django.test import TestCase
import cria_coworking.models as ccm  # cria coworking models
from gere_coworking.models import *
import domains.models as dm  # domains models

import datetime


class TestGereCoworkingModels(TestCase):
    def setUp(self):
        self.cliente_user = self.user = User.objects.create_user(
            username='309.940.155-26',
            password='newgen123',
            email='tiagocavalcantiribeiro@gmail.com',
            first_name='Tiago',
            last_name='Ribeiro',
            is_superuser=False,
            is_staff=False)
        self.funcionario_user = self.user = User.objects.create_user(
            username='837.822.262-40',
            password='newgen123',
            email='rebecalimaazevedo@teleworm.us',
            first_name='Rebeca',
            last_name='Azevedo',
            is_superuser=False,
            is_staff=True)
        self.cliente = ClienteModel.objects.create(
            nome='Tiago Ribeiro',
            # senha = 'newgen123',
            cpf_cnpj='309.940.155-26',
            data_nascimento='1986-09-12',
            genero='M',
            email='tiagocavalcantiribeiro@gmail.com',
            telefone='11977866159',
            cep='04611-060',
            logradouro='Rua Alberto Gebara',
            numero='1604',
            bairro='Parque Colonial',
            cidade='São Paulo',
            estado='SP',
            user=self.cliente_user
        )
        self.funcionario = FuncionariosModel.objects.create(
            nome='Rebeca Azevedo',
            # senha = 'newgen123',
            cpf_cnpj='837.822.262-40',
            data_nascimento='1928-06-12',
            genero='F',
            email='rebecalimaazevedo@teleworm.us',
            telefone='11995953275',
            cep='60710-840',
            logradouro='Rua Otávio Filomeno',
            numero='108',
            bairro='Maraponga',
            cidade='Fortaleza',
            estado='CE',
            user=self.funcionario_user
        )
        self.tipoespaco = TipoespacoModel.objects.create(
            descricao='descricao',
            nome='Mesa compartilhada',
            ultima_alteracao=self.funcionario,
            tempo_limpeza="00:03:00",
            preco=42.4,
            data_ultima_alteracao='2021-06-12 06:00:00.000000-03:00',
            compartilhado=1,
        )
        self.equipamento = EquipamentosModel.objects.create(
            tipo='câmera',
            descrição='Nikon D3100 DSLR cor preto',
            preco=30,
            ultima_alteracao=self.funcionario,
            status_equipamento="0",
            data_ultima_alteracao='2021-10-07 18:40:00.000000-03:00',
        )
        self.pacotehora = PacotehorasModel.objects.create(
            id_cliente=self.cliente,
            qtd_horas=20,
            id_empresa=self.cliente,
            status_pacotehoras=1
        )
        self.espaco = EspacosModel.objects.create(
            id_tipo_espaco=self.tipoespaco,
            ultima_alteracao=self.funcionario,
            status_espaco=1,
            data_ultima_alteracao='2021-05-07 18:40:00.000000-03:00',
        )
        self.reserva = ReservaModel.objects.create(
            id_cliente=self.cliente,
            id_pagamento=None,
            id_espaco=self.espaco,
            id_pacote_horas=self.pacotehora,
            data_reserva='2021-05-07',
            hora_entrada='15:00:00',
            hora_saida='17:00:00',
            hora_limpeza='17:15:00',
            datahora_log='2021-05-05 18:40:00.000000-03:00',
            hora_entrada_real='14:54:00',
            hora_saida_real='16:37:00',
            hora_limpeza_real='17:00:17',
            preco_total=50,
        )
        # self.advertencia = AdvertenciasModel.objects.create(
        #     comentario = 'Mesa bagunçada',
        #     # id_reserva = self.reserva,
        #     # id_funcionario = self.funcionario,
        # )
        self.pagamento = PagamentoModel.objects.create(
            metodo='PIX',
            cod_mercadopago=981981,
            status_pagamento="1",
            datahora_log='2021-05-05 19:40:00.000000-03:00',
            # id_reserva = self.reserva,
            id_equipamento=self.equipamento
        )
        self.convidados = ConvidadosModel.objects.create(
            id_reserva=self.reserva,
            id_cliente=self.cliente,
            email='douglasaguzman@cuvox.de'
        )
        self.equipamentoreserva = EquipamentoreservaModel.objects.create(
            id_reserva=self.reserva,
            id_equipamento=self.equipamento,
            preco_locacao_equipamento=30,
            id_pagamento=self.pagamento,
        )

    def test_cliente_model(self):
        self.assertEquals(self.cliente.nome, 'Tiago Ribeiro')
        self.assertEquals(self.cliente.cpf_cnpj, '309.940.155-26')
        self.assertEquals(self.cliente.data_nascimento, '1986-09-12')
        self.assertEquals(self.cliente.genero, 'M')
        self.assertEquals(self.cliente.email, 'tiagocavalcantiribeiro@gmail.com')
        self.assertEquals(self.cliente.telefone, '11977866159')
        self.assertEquals(self.cliente.cep, '04611-060')
        self.assertEquals(self.cliente.logradouro, 'Rua Alberto Gebara')
        self.assertEquals(self.cliente.numero, '1604')
        self.assertEquals(self.cliente.bairro, 'Parque Colonial')
        self.assertEquals(self.cliente.cidade, 'São Paulo')
        self.assertEquals(self.cliente.estado, 'SP')

    def test_funcionario_model(self):
        self.assertEquals(self.funcionario.nome, 'Rebeca Azevedo')
        self.assertEquals(self.funcionario.cpf_cnpj, '837.822.262-40')
        self.assertEquals(self.funcionario.data_nascimento, '1928-06-12')
        self.assertEquals(self.funcionario.genero, 'F')
        self.assertEquals(self.funcionario.email, 'rebecalimaazevedo@teleworm.us')
        self.assertEquals(self.funcionario.telefone, '11995953275')
        self.assertEquals(self.funcionario.cep, '60710-840')
        self.assertEquals(self.funcionario.logradouro, 'Rua Otávio Filomeno')
        self.assertEquals(self.funcionario.numero, '108')
        self.assertEquals(self.funcionario.bairro, 'Maraponga')
        self.assertEquals(self.funcionario.cidade, 'Fortaleza')
        self.assertEquals(self.funcionario.estado, 'CE')

    def test_tipoespaco_model(self):
        self.assertEquals(self.tipoespaco.descricao, 'descricao')
        self.assertEquals(self.tipoespaco.nome, 'Mesa compartilhada')
        self.assertEquals(self.tipoespaco.ultima_alteracao, self.funcionario)
        self.assertEquals(self.tipoespaco.tempo_limpeza, "00:03:00")
        self.assertEquals(self.tipoespaco.preco, 42.4)
        # self.assertEquals(self.tipoespaco.data_ultima_alteracao, '2021-06-12 06:00:00.000000-03:00')
        self.assertEquals(self.tipoespaco.compartilhado, True)

    def test_equipamentos_model(self):
        self.assertEquals(self.equipamento.tipo, 'câmera')
        self.assertEquals(self.equipamento.descrição, 'Nikon D3100 DSLR cor preto')
        self.assertEquals(self.equipamento.preco, 30)
        self.assertEquals(self.equipamento.ultima_alteracao, self.funcionario)
        self.assertEquals(self.equipamento.status_equipamento, "0")
        self.assertEquals(self.equipamento.data_ultima_alteracao, '2021-10-07 18:40:00.000000-03:00')

    def test_pacote_hora_model(self):
        self.assertEquals(self.pacotehora.id_cliente, self.cliente)
        self.assertEquals(self.pacotehora.qtd_horas, 20)
        self.assertEquals(self.pacotehora.id_empresa, self.cliente)
        self.assertEquals(self.pacotehora.status_pacotehoras, 1)

    def test_espacos_model(self):
        self.assertEquals(self.espaco.id_tipo_espaco, self.tipoespaco)
        self.assertEquals(self.espaco.ultima_alteracao, self.funcionario)
        self.assertEquals(self.espaco.status_espaco, 1)
        self.assertEquals(self.espaco.data_ultima_alteracao, '2021-05-07 18:40:00.000000-03:00')

    def test_reserva_model(self):
        self.assertEquals(self.reserva.id_cliente, self.cliente)
        self.assertEquals(self.reserva.id_pagamento, None)
        self.assertEquals(self.reserva.id_espaco, self.espaco)
        self.assertEquals(self.reserva.id_pacote_horas, self.pacotehora)
        self.assertEquals(self.reserva.data_reserva, '2021-05-07')
        self.assertEquals(self.reserva.hora_entrada, '15:00:00')
        self.assertEquals(self.reserva.hora_saida, '17:00:00')
        self.assertEquals(self.reserva.hora_limpeza, '17:15:00')
        self.assertEquals(self.reserva.datahora_log, '2021-05-05 18:40:00.000000-03:00')
        self.assertEquals(self.reserva.hora_entrada_real, '14:54:00')
        self.assertEquals(self.reserva.hora_saida_real, '16:37:00')
        self.assertEquals(self.reserva.hora_limpeza_real, '17:00:17')
        self.assertEquals(self.reserva.preco_total, 50)

    # def test_advertencia_model(self):
    #     self.assertEquals(self.advertencia.comentario, 'Mesa bagunçada')
    #     self.assertEquals(self.advertencia.id_reserva, self.reserva)
    #     self.assertEquals(self.advertencia.id_funcionario, self.funcionario)

    def test_pagamento_model(self):
        self.assertEquals(self.pagamento.metodo, 'PIX')
        self.assertEquals(self.pagamento.cod_mercadopago, 981981)
        self.assertEquals(self.pagamento.status_pagamento, "1")
        # self.assertEquals(self.pagamento.datahora_log, '2021-05-05 19:40:00.000000-03:00')
        # self.assertEquals(self.pagamento.id_reserva, self.reserva)
        self.assertEquals(self.pagamento.id_equipamento, self.equipamento)

    def test_convidados_model(self):
        self.assertEquals(self.convidados.id_reserva, self.reserva)
        self.assertEquals(self.convidados.id_cliente, self.cliente)
        self.assertEquals(self.convidados.email, 'douglasaguzman@cuvox.de')

    def test_equipamentoreserva_model(self):
        self.assertEquals(self.equipamentoreserva.id_reserva, self.reserva)
        self.assertEquals(self.equipamentoreserva.id_equipamento, self.equipamento)
        self.assertEquals(self.equipamentoreserva.preco_locacao_equipamento, 30)
        self.assertEquals(self.equipamentoreserva.id_pagamento, self.pagamento)


class TestCriaCoworkingModels(TestCase):
    def setUp(self):
        self.domain = dm.Domain.objects.create(
            domain='test.com',
            name='test',
            isActive=1,
        )

        self.administrador = ccm.Administrador.objects.create(
            nome='Newgen',
            cnpj='68.024.572/0001-44',
            email='newgen@gmail.com',
            telefone='11977866159',
            cep='68904-340',
            logradouro='Avenida Guajarina Duarte Mendes',
            numero='1450',
            bairro='Congós',
            cidade='Macapá',
            estado='AP',
            database='newgen981981db',
            domain=self.domain
        )

    def test_domain_model(self):
        self.assertEquals(self.domain.domain, 'test.com')
        self.assertEquals(self.domain.name, 'test')
        self.assertEquals(self.domain.isActive, 1)

    def test_administrador_model(self):
        self.assertEquals(self.administrador.nome, 'Newgen')
        self.assertEquals(self.administrador.cnpj, '68.024.572/0001-44')
        self.assertEquals(self.administrador.email, 'newgen@gmail.com')
        self.assertEquals(self.administrador.telefone, '11977866159')
        self.assertEquals(self.administrador.cep, '68904-340')
        self.assertEquals(self.administrador.logradouro, 'Avenida Guajarina Duarte Mendes')
        self.assertEquals(self.administrador.numero, '1450')
        self.assertEquals(self.administrador.bairro, 'Congós')
        self.assertEquals(self.administrador.cidade, 'Macapá')
        self.assertEquals(self.administrador.estado, 'AP')
        self.assertEquals(self.administrador.database, 'newgen981981db')
        self.assertEquals(self.administrador.domain, self.domain)
