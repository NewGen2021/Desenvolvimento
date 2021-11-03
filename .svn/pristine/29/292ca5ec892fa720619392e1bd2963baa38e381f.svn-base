import gere_coworking.models as m
import cria_coworking.models as m2
import datetime, sys

def get_reservas_cliente(cpf_cnpj, id_tipo_espaco=None):
    cliente = list(m.ClienteModel.objects.filter(
            cpf_cnpj = cpf_cnpj
        ))[0]
    if id_tipo_espaco is None:
        reservas = m.ReservaModel.objects.filter(
            id_cliente=cliente.id_cliente,
            data_reserva__gte=datetime.datetime.now().date()
        )
        return reservas
    else:
        espacos = m.EspacosModel.objects.filter(
        id_tipo_espaco = id_tipo_espaco
        ).order_by('id_tipo_espaco')
        espacos_id = []
        # espacos_id = [2, 3, 4, 7] // por exemplo
        for espaco in espacos:
            espacos_id.append(espaco.id_espaco)
        reservas = []
        for espaco_id in espacos_id:
            reservas += list( 
                    m.ReservaModel.objects.filter(
                    id_espaco = espaco_id,
                    id_cliente=cliente.id_cliente,
                    data_reserva__gte=datetime.datetime.now().date()
                    ).order_by('data_reserva')
                )
    return reservas

def get_reservas_atuais(id_tipo_espaco):
    espacos = m.EspacosModel.objects.filter(
        id_tipo_espaco = id_tipo_espaco
    ).order_by('id_tipo_espaco')
    espacos_id = []
    # espacos_id = [2, 3, 4, 7] // por exemplo
    for espaco in espacos:
        espacos_id.append(espaco.id_espaco)
    reservas = []
    for espaco_id in espacos_id:
        reservas += list( 
                m.ReservaModel.objects.filter(
                id_espaco = espaco_id,
                data_reserva__gte=datetime.datetime.now().date()
                ).order_by('data_reserva')
            )
    return reservas

def is_cliente_duplicated(cpf_cnpj, tipo_pessoa="cliente"):
    if tipo_pessoa == 'cliente':
        return m.ClienteModel.objects.filter(
            cpf_cnpj = cpf_cnpj
        ).exists()
    if tipo_pessoa == 'funcionario':
        return m.FuncionariosModel.objects.filter(
            cpf_cnpj = cpf_cnpj
        ).exists()
    if tipo_pessoa == 'administrador':
        return m2.Administrador.objects.filter(
            cnpj = cpf_cnpj
        ).exists()
    return False