'''
    * Métodos usados especificamente na funcionalidade de reservas
    * Favor manter em ordem alfabética
'''

from typing import OrderedDict
import gere_coworking.views.views_helper as h
from gere_coworking.models.models import TipoespacoModel, ReservaModel, ClienteModel, EspacosModel
import datetime, sys
from django.utils.translation import gettext as _

businessHours = [{
        # days of week. an array of zero-based day of week integers (0=Sunday)
        'daysOfWeek': [ 1, 2, 3, 4, 5 ], # Monday - Friday

        'startTime': '07:00', # a start time (07:00, 07:30, 08:00) (7am in this example)
        'endTime': '22:00', # an end time (10pm in this example)
        },
        {
            'daysOfWeek': [ 6, 0 ], # Saturday, Sunday
            'startTime': '09:00', # a start time (9am in this example)
            'endTime': '19:00', # an end time (7pm in this example)
        }]

def converteNumeroDiaSemana(weekday, To_ISO=True):
    # ISO-8601 [0 - monday, 1 - tuesday, 6 - sunday]
    # Não ISO [0 - sunday , 1 - monday , 6 - saturday]
    if To_ISO:
        if weekday == 0:
            return 6
        return weekday - 1
    else:
        if weekday == 6:
            return 0
        return weekday + 1
    

def createDayDict(diaSemana):
    dicionario = getDicionarioBusinessHours(diaSemana)
    dayDict = {}
    hora = datetime.datetime.strptime(dicionario['startTime'], "%H:%M")
    horaFim = datetime.datetime.strptime(dicionario['endTime'], "%H:%M")

    while hora <= horaFim:
        dayDict[hora.strftime("%H:%M")] = 0
        hora += datetime.timedelta(minutes=30)
    return dayDict

def getDicionarioBusinessHours(diaSemana):
    for dicionario in businessHours:
        if diaSemana in dicionario['daysOfWeek']:
            return dicionario
    raise ValueError('O diaSemana da getDicionarioBusinessHours tem que ser um número de 0 até 6. diaSemana informado = ' + str(diaSemana))

def getDicionarioReservas(id_tipo_espaco):
    dateDicts = {}
    
    datasRastreadas = []
    reservas = getReservasAtuais(id_tipo_espaco)

    # Popula o dicionário
    for reserva in reservas:
        data = reserva.data_reserva
        diaSemana = converteNumeroDiaSemana(data.weekday(), To_ISO=False)

        # Cria um novo dicionário de horas para uma data caso ela não exista
        if data not in datasRastreadas:
            datasRastreadas.append(data)
            dateDicts[data.strftime("%Y-%m-%d")] = createDayDict(diaSemana)

        # Marca as horas desta reserva no dicionário
        entrada = datetime.datetime.combine(reserva.data_reserva, reserva.hora_entrada)
        saida = datetime.datetime.combine(reserva.data_reserva, reserva.hora_saida)
        
        dicionario = getDicionarioBusinessHours(diaSemana)
        hour, minute = dicionario['startTime'].split(':')
        
        hora = entrada
        horaJson = entrada
        
        horaJson = entrada.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        while hora < saida:
            if entrada <= horaJson:
                hora += datetime.timedelta(minutes=30)
                # Incrementa o campo do JSON com um valor a mais
                dateDicts[data.strftime("%Y-%m-%d")][horaJson.strftime("%H:%M")] += 1
            horaJson += datetime.timedelta(minutes=30)
    return dateDicts
    # dateDicts = {'2021-07-28': {
    #     '07:00': 0,
    #     '07:30': 1,
    #     '08:00': 1,
    #     '08:30': 1,
    #     '09:00': 0
    # }}, {'2021-07-31': {
    #     '07:00': 0,
    #     '07:30': 1,
    #     '08:00': 1,
    #     '08:30': 1,
    #     '09:00': 0
    # }}

# Não deletar
def getDicionarioReservasDia(id_espaco, dia, reservas=None):
    
    # reservas = getReservasAtuaisDia(id_tipo_espaco, dia)
    if reservas is None:
        reservas = ReservaModel.objects.filter(id_espaco= EspacosModel.objects.get(id_espaco=id_espaco), data_reserva=dia)
    if type(dia) == str:
        diaSemana = converteNumeroDiaSemana(datetime.datetime.strptime(dia, "%Y-%m-%d").weekday(), To_ISO=False)
    else:
        diaSemana = converteNumeroDiaSemana(dia.weekday(), To_ISO=False)
    dicio = createDayDict(diaSemana)

    # Popula o dicionário
    for reserva in reservas:
        # Marca as horas desta reserva no dicionário
        if type(reserva) == dict:
            entrada = f"{reserva['data_reserva']}T{reserva['hora_entrada']}"
            entrada = datetime.datetime.strptime(entrada, "%Y-%m-%dT%H:%M:%S")
            saida = f"{reserva['data_reserva']}T{reserva['hora_saida']}"
            saida = datetime.datetime.strptime(saida, "%Y-%m-%dT%H:%M:%S")
        else:
            entrada = datetime.datetime.combine(reserva.data_reserva, reserva.hora_entrada)
            saida = datetime.datetime.combine(reserva.data_reserva, reserva.hora_saida)
        
        dicionario = getDicionarioBusinessHours(diaSemana)
        hour, minute = dicionario['startTime'].split(':')
        
        hora = entrada
        horaJson = entrada
        
        horaJson = entrada.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        while hora < saida:
            if entrada <= horaJson:
                hora += datetime.timedelta(minutes=30)
                # Incrementa o campo do JSON com um valor a mais
                dicio[horaJson.strftime("%H:%M")] += 1
            horaJson += datetime.timedelta(minutes=30)
    return dicio

def getPorcentagemOcupadaDia(date_dict, max_vaga):
    ocupado_points = 0
    total = 0
    for value in date_dict.values():
        total += max_vaga
        ocupado_points += value
    return ocupado_points/total

def getEventoMes(porcentagem: float, cores: tuple, date: str):
    divisao = 100/(len(cores)-1)
    i = int(porcentagem//divisao)
    return {
        'start': f'{date}T01:00:00',
        'end': f'{date}T23:00:00',
        'color': cores[i][0],
        'textColor': cores[i][1],
    }

    return


def getEventoReservasCliente(request, id_tipo_espaco):
    event_list = []
    if h.isAdministrator(request=request):
        return event_list
    # Se houver algum tipo de espaço definido
    if id_tipo_espaco != 0:
        reservas = getReservasCliente(request, request.user.username, id_tipo_espaco)
    else:
        reservas = getReservasCliente(request=request, cpf_cnpj=request.user.username)
    for reserva in reservas:
        inicioReserva = datetime.datetime.combine(reserva.data_reserva, reserva.hora_entrada)
        fimReserva = datetime.datetime.combine(reserva.data_reserva, reserva.hora_saida)
        event_list.append({
                    'title': _('Sua reserva') if id_tipo_espaco else f'{getReservaTipoEspacoName(reserva.id_espaco)}',
                    'start': inicioReserva.strftime("%Y-%m-%dT%H:%M:%S"),
                    'end': fimReserva.strftime("%Y-%m-%dT%H:%M:%S"),
                    'color': 'lightblue',
                    'textColor': 'black',
                    # 'display': 'list-item'
                })
    return event_list

def getEventoReservasLotadas(dateDicts, vagas_max, event_list):
    for data, horarios in dateDicts.items():
        comecoEvento = False # Lógica de verificação do começo do evento
        inicio = None # Para salvar o horário do começo do evento
        
        # Lê as horas de um dia das reservas
        for hora, valor in horarios.items():

            # Começa a rastrear o tamanho do evento
            if valor >= vagas_max and comecoEvento == False:
                comecoEvento = True
                inicio = hora

            # Conclui o fim do evento e define a lógica de setar o evento
            if comecoEvento == True and valor < vagas_max :
                comecoEvento = False
                fim = hora

                ##############################################################################################
                # Confere os eventos de reserva do cliente para dar prioridade pro evento do cliente na tela 
                ##############################################################################################
                reservasDoDia = []

                # Separa os eventos relativos ao dia que se quer analisar
                for evento in event_list:
                    dataEvento = datetime.datetime.strptime(evento['start'], "%Y-%m-%dT%H:%M:%S").replace(hour=0, minute=0, second=0, microsecond=0)
                    dataAtual = datetime.datetime.strptime(data, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
                    if dataEvento == dataAtual:
                        reservasDoDia.append(evento)

                # Evento lotado = evento que há indisponibilidade de vagas (cor vermelha)
                # Reserva neste contexto = reserva do cliente no dia (cor azul)
                for evento in reservasDoDia:
                    comecoReserva = datetime.datetime.strptime(evento['start'], "%Y-%m-%dT%H:%M:%S").replace(year=2020, month=1, day=1)
                    fimReserva = datetime.datetime.strptime(evento['end'], "%Y-%m-%dT%H:%M:%S").replace(year=2020, month=1, day=1)
                    comecoEventoLotado = datetime.datetime.strptime(inicio, "%H:%M").replace(year=2020, month=1, day=1)
                    fimEventoLotado = datetime.datetime.strptime(fim, "%H:%M").replace(year=2020, month=1, day=1)

                    if comecoReserva <= comecoEventoLotado and comecoEventoLotado <= fimReserva:
                        inicio = fimReserva.strftime("%H:%M")
                    if comecoReserva <= fimEventoLotado and comecoEventoLotado <= fimReserva:
                        fim = comecoReserva.strftime("%H:%M")
                ##############################################################################################

                ano, mes, dia = data.split('-')
                hour, minutes = inicio.split(':')
                start = f'{ano}-{mes}-{dia}T{hour}:{minutes}:00'
                hour, minutes = fim.split(':')
                end = f'{ano}-{mes}-{dia}T{hour}:{minutes}:00'
                # print('------------- VARS', file=sys.stderr)
                # print(start, file=sys.stderr)
                # print(end, file=sys.stderr)
                event_list.append({
                    'title': _('Sem vagas'),
                    'start': start,
                    'end': end,
                    'color': 'red',
                    'textColor': 'black',
                    # 'display': 'list-item'
                })
    return event_list

# Não deletar
def getEventoReservasLotadasViewSet(dateDict, vagas_max, event_list, date):        
    """ dateDict={'07:00': 0, '07:30': 0, '08:00': 0, '08:30': 0, '09:00': 0, '09:30': 0,
     '10:00': 0, '10:30': 0, '11:00': 0, '11:30': 0, '12:00': 0, '12:30': 0, '13:00': 1,
      '13:30': 1, '14:00': 2, '14:30': 2, '15:00': 1, '15:30': 1, '16:00': 0, '16:30': 0,
       '17:00': 0, '17:30': 0, '18:00': 0, '18:30': 0, '19:00': 0, '19:30': 0, '20:00': 0,
        '20:30': 0, '21:00': 0, '21:30': 0, '22:00': 0} """
    
    """ event_list = [{'title': 'Sua reserva',
                   'start': '2021-10-13T13:00:00',
                   'end': '2021-10-13T15:00:00',
                   'color': 'lightblue',
                   'textColor': 'black'}] """

    # Seta o horário para 0 no dateDict caso seja uma reserva do usuário
    for reserva_cliente in event_list:
        hora_inicio = reserva_cliente['start'].split('T')[1] # 13:00:00
        hora_fim = reserva_cliente['end'].split('T')[1] # 15:00:00
        
        for hora in dateDict.keys():
            if hora >= hora_inicio and hora <= hora_fim:
                dateDict[hora] = 0
    
    comecoEvento = False # Lógica de verificação do começo do evento
    inicio = None # Para salvar o horário do começo do evento

    # Lê as horas de um dia das reservas
    for hora, valor in dateDict.items():

        # Começa a rastrear o tamanho do evento
        if valor >= vagas_max and comecoEvento == False:
            comecoEvento = True
            inicio = hora

        # Conclui o fim do evento e define a lógica de setar o evento
        if comecoEvento == True and valor < vagas_max :
            comecoEvento = False
            fim = hora

            event_list.append({
                    'title': _('Sem vagas'),
                    'start': f'{date}T{inicio}:00',
                    'end': f'{date}T{fim}:00',
                    'color': 'red',
                    'textColor': 'black',
                })
        
    return event_list

def getForm(request, id_tipo_espaco):
    hora_entrada = request.POST['hora-entrada'].split(' ')[0]
    hora_saida = request.POST['hora-saida'].split(' ')[0]

    ''' revisar '''
    if isCompartilhado(id_tipo_espaco):
        id_espaco = 1
    else:
        id_espaco = request.POST['id_espaco']

    hora_limpeza = getHoraLimpeza(id_espaco, hora_saida)

    cliente = list(ClienteModel.objects.filter(
        cpf_cnpj = request.user.username
    ))[0]
    
    # hoje = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    hoje = datetime.datetime.today()
    preco = getPrecoEspaco(id_espaco)
    dicionario = {
        'id_cliente': cliente.id_cliente,
        'id_espaco': id_espaco,
        'data_reserva': request.POST['data-reserva'],
        'hora_entrada': hora_entrada,
        'hora_saida': hora_saida,
        'hora_limpeza': hora_limpeza.strftime("%H:%M:%S"),
        'datahora_log': hoje,
        'hora_entrada_real': '',
        'hora_saida_real': '',
        'hora_limpeza_real': '',
        'preco_total': preco,
        }
    return dicionario

def getFormErrors(dicionario, event_list):
    hora_entrada = datetime.datetime.strptime(dicionario['hora_entrada'], "%H:%M:%S")
    hora_saida = datetime.datetime.strptime(dicionario['hora_saida'], "%H:%M:%S")
    dataReserva = datetime.datetime.strptime(dicionario['data_reserva'], "%d/%m/%Y")
    hoje = datetime.datetime.today()
    error = None
    hasErrors = False

    if hora_entrada > hora_saida:
        hasErrors = True
        error = _('ERRO! A hora de entra não pode ser menor que a hora de saída.')
    elif dataReserva < hoje:
        hasErrors = True
        error = _('ERRO! A data informada já passou!')
    elif (hora_saida - hora_entrada) < datetime.timedelta(minutes=30):
        hasErrors = True
        error = _('ERRO! O tempo mínimo de reserva é 30 minutos.')
    elif (dataReserva - hoje) > datetime.timedelta(days=30):
        hasErrors = True
        error = _('ERRO! Não é possível realizar reservas de forma programática para mais de 30 dias. Entre em contato conosco.')
    else:
        # Confere os eventos reservados
        for evento in event_list:
            hora, minuto, segundo = dicionario['hora_entrada'].split(':')
            dhora_entrada = datetime.datetime.combine(dataReserva, datetime.time(int(hora), int(minuto), int(segundo)))
            hora, minuto, segundo = dicionario['hora_saida'].split(':')
            dhora_saida = datetime.datetime.combine(dataReserva, datetime.time(int(hora), int(minuto), int(segundo)))
            inicioEvento = datetime.datetime.strptime(evento['start'], '%Y-%m-%dT%H:%M:%S')
            fimEvento = datetime.datetime.strptime(evento['end'], '%Y-%m-%dT%H:%M:%S')
            if (inicioEvento < dhora_entrada and dhora_entrada < fimEvento) or (inicioEvento < dhora_saida and dhora_saida < fimEvento):
                hasErrors = True
                error = _('Horário já reservado. Escolha outro.')
                break
        diaSemana = dataReserva.weekday()

        # Converte dia da semana para modelo do full calendar
        if diaSemana == 6:
            diaSemana = 0
        else:
            diaSemana += 1
        
        # Confere se a hora está dentro do horário comercial válido
        for dicionario in businessHours:
            if diaSemana in dicionario['daysOfWeek']:
                horarioAbertura = datetime.datetime.strptime(dicionario['startTime'], "%H:%M")
                horarioFechamento = datetime.datetime.strptime(dicionario['endTime'], "%H:%M")
                if (hora_entrada < horarioAbertura) or (hora_saida > horarioFechamento):
                    hasErrors = True
                    error = _('Fora de horário comercial, tente outro horário.')
                break
    return hasErrors, error

def getHoraLimpeza(id_espaco, hora_saida):
    espaco = list(EspacosModel.objects.filter(
        id_espaco = id_espaco
    ))[0]
    hora, minuto, segundo = hora_saida.split(':')
    dataHoraSaida = datetime.datetime.today().replace(hour=int(hora), minute=int(minuto), second=int(segundo))
    hourDelta, minDelta, segDelta = espaco.id_tipo_espaco.tempo_limpeza.strftime("%H %M %S").split(' ')
    hora_limpeza = dataHoraSaida + datetime.timedelta(hours=int(hourDelta), minutes=int(minDelta), seconds=int(segDelta))
    return hora_limpeza

def getPrecoEspaco(id_espaco):
    espaco = list(EspacosModel.objects.filter(
        id_espaco = id_espaco
    ))[0]
    return espaco.id_tipo_espaco.preco

def getReservasAtuais(id_tipo_espaco):
    return ReservaModel.objects.get_reservas_atuais(id_tipo_espaco = id_tipo_espaco)

def getReservasAtuaisMes(mes: int, id_espaco: int):
    date = datetime.datetime.today().date()
    reservas = []
    while date.month == mes:
        reservas += ReservaModel.objects.filter(id_espaco=id_espaco, data_reserva=date)
        date += datetime.timedelta(days=1)
    return reservas


def getReservasCliente(request, cpf_cnpj, id_tipo_espaco=None):
    if id_tipo_espaco:
        return ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username, id_tipo_espaco = id_tipo_espaco)
    return ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username)

def getReservaTipoEspacoName(id_espaco):
    reserva = list(ReservaModel.objects.filter(
        id_espaco = id_espaco
    ))[0]
    return reserva.id_espaco.id_tipo_espaco.nome

def get_vagas_dict(date_dict, max_vagas):
    for hora in date_dict.keys():
        vagas_ocupadas = date_dict[hora]
        date_dict[hora] = max_vagas - vagas_ocupadas
    return date_dict

def isCompartilhado(id_tipo_espaco):
    return list(TipoespacoModel.objects.filter(
            id_tipoespaco = id_tipo_espaco
        ))[0].compartilhado
