from rest_framework import (viewsets, generics)
from rest_framework.views import APIView
from rest_framework import status
from cria_coworking.models import Administrador
from custom_templates.models import ResourceButtons
from gere_coworking.models import (ReservaModel, EspacosModel, PagamentoModel, TipoespacoModel)
from . import serializers
from django.utils.translation import gettext as _
from gere_coworking.services.reserva import (getDicionarioReservasDia, getEventoReservasCliente,
                                             getEventoReservasLotadasViewSet, get_vagas_dict, getReservasAtuaisMes,
                                             getPorcentagemOcupadaDia, getEventoMes)
from datetime import *
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
import common.services_modules.pagamento as b_pagamento  # 'b' de 'business"
import common.models_choices as mc
from common.selectors import get_administrador_logado_in_cria
from django.conf import settings
import mercadopago

sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

VAGAS_DEFAULT = 2


# class ProtectedView(TemplateView):
#     template_name = 'secret.html'

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)


class PagamentoAPIView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @staticmethod
    def get(request):
        print('GETTTTTTTTTTTTTTTTT')
        print(request.data)
        pagamentos = PagamentoModel.objects.all()
        serializer = serializers.PagamentoSerializer(pagamentos, many=True)
        return Response(serializer.data)

    # @csrf_exempt
    @staticmethod
    def post(request):
        id_reserva = request.data.pop('id_reserva')
        pagamento = b_pagamento.efetuar_pagamento(request)

        # json = {
        #     "metodo": "Cartão de Débito",
        #     "cod_mercadopago": 65117,
        #     "status_pagamento": 1,
        #     "id_reserva": 2,
        # }
        print('VIEWSETTTTTTTTTTTTTTTTTO')
        print(pagamento)
        print(request.data)
        # try:
        #     pagamento = PagamentoModel.objects.get(id_reserva=ReservaModel.objects.get(id_reserva=981))
        #     PagamentoModel.objects.update_or_create
        # except ReservaModel.DoesNotExist:
        #     pagamento = PagamentoModel.objects.create(metodo="Cartão de Débito", cod_mercadopago=65117, status_pagamento=1, id_reserva=ReservaModel(id_reserva=2))
        metodo = pagamento.get('payment_type_id')
        cod_mercadopago = pagamento.get('id')
        status_pagamento = pagamento.get('status')
        for choice in mc.PAGAMENTO_STATUS_CHOICES:
            print(choice, status_pagamento)
            if choice[1] == status_pagamento:
                status_pagamento = choice[0]
                break

        pag = PagamentoModel.objects.create(metodo=metodo if metodo else 'failed',
                                            cod_mercadopago=cod_mercadopago if cod_mercadopago else 0,
                                            status_pagamento=status_pagamento if status_pagamento else 0)
        # TODO
        aluguel = True
        if aluguel:
            ReservaModel.objects.filter(id_reserva=id_reserva).update(is_aluguel=True, id_pagamento=pag.id_pagamento)
        # pagamentos = PagamentoModel.objects.all()
        # serializer = serializers.PagamentoSerializer(pagamentos, many=True)

        erro = pagamento.get('message')
        mensagem_de_erro = erro if erro else 'none'
        return Response(data={'mensagem_de_erro': mensagem_de_erro}, status=status.HTTP_201_CREATED)


class BasicReservaViewset(viewsets.ModelViewSet):
    queryset = ReservaModel.objects.all()
    serializer_class = serializers.ReservaSerializer


class ReservaDateViewset(generics.ListAPIView):
    serializer_class = serializers.ReservaSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        data_reserva = self.kwargs['data_reserva']
        return ReservaModel.objects.filter(data_reserva=data_reserva)


class ReservaIdViewset(generics.ListAPIView):
    serializer_class = serializers.ReservaHashSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id_reserva = self.kwargs['id_reserva']
        return ReservaModel.objects.filter(id_reserva=id_reserva)


class TipoEspacoGetPrecoViewset(generics.ListAPIView):
    serializer_class = serializers.TipoEspacoPrecoSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id_tipo_espaco = self.kwargs['id_tipo_espaco']
        return TipoespacoModel.objects.filter(id_tipoespaco=id_tipo_espaco)


class ReservaEventDateViewset(generics.ListAPIView):
    serializer_class = serializers.ReservaSerializer

    def __init__(self):
        self.COR_RESERVA_USUARIO = ('lightblue', 'black')
        self.COR_RESERVA_OUTRA = ('red', 'black')

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        data_reserva = self.kwargs['data_reserva']
        id_espaco = self.kwargs['id_espaco']

        return ReservaModel.objects.filter(data_reserva=data_reserva, id_espaco=id_espaco)

    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(ReservaEventDateViewset, self).list(request, *args, **kwargs)
        if not response.data:
            return response
        data_reserva = self.kwargs['data_reserva']
        id_cliente = int(self.kwargs['id_cliente'])
        id_espaco = int(self.kwargs['id_espaco'])
        id_tipo_espaco = EspacosModel.objects.get(id_espaco=id_espaco).id_tipo_espaco
        self.is_compartilhado = EspacosModel.objects.get(id_espaco=id_espaco).id_tipo_espaco.compartilhado

        reservas = response.data
        response.data = {'event_list': [], 'vagas_dict': {}}

        """
        reservas = [
            {
                "id_reserva": 2,
                "id_cliente": 1,
                "data_reserva": "2021-10-13",
                "hora_entrada": "13:00:00",
                "hora_saida": "15:00:00"
            }
        ] """

        if self.is_compartilhado:
            event_list = []
            for reserva in reservas:
                reserva_do_usuario = id_cliente == reserva['id_cliente']
                if reserva_do_usuario:
                    event_list.append(self.get_dict_event_format(reserva, reserva_do_usuario))
            # event_list = getEventoReservasCliente(request, id_tipo_espaco)
            date_dict = getDicionarioReservasDia(id_espaco, data_reserva)
            try:
                vagas = EspacosModel.objects.get(id_espaco=self.id_espaco).vagas
            except AttributeError:
                vagas = VAGAS_DEFAULT
            response.data['event_list'] = getEventoReservasLotadasViewSet(date_dict, vagas, event_list, data_reserva)
            response.data['vagas_dict'] = get_vagas_dict(date_dict, vagas)
        else:
            for reserva in reservas:
                reserva_do_usuario = id_cliente == reserva['id_cliente']
                response.data['event_list'].append(self.get_dict_event_format(reserva, reserva_do_usuario))

        return response

    def get_dict_event_format(self, reserva, reserva_do_usuario):
        return {
            'title': _('Sua reserva') if reserva_do_usuario else _('Reservado'),
            'start': f'{reserva["data_reserva"]}T{reserva["hora_entrada"]}',
            'end': f'{reserva["data_reserva"]}T{reserva["hora_saida"]}',
            'color': self.COR_RESERVA_USUARIO[0] if reserva_do_usuario else self.COR_RESERVA_OUTRA[0],
            'textColor': self.COR_RESERVA_USUARIO[1] if reserva_do_usuario else self.COR_RESERVA_OUTRA[1],
            'compartilhado': self.is_compartilhado
        }


class ReservaEventMonthViewset(generics.ListAPIView):
    serializer_class = serializers.ReservaSerializer

    def __init__(self):
        # vazio = sem cor
        self.COR_RESERVA_USUARIO = ('lightblue', 'black')
        self.CORES_OCUPADO = (('green', 'black'), ('yellow', 'black'), ('orange', 'black'), ('red', 'black'))

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mes = self.kwargs['mes'].split('-')  # '2021-10'
        self.ano, self.mes = int(mes[0]), int(mes[1])
        self.id_espaco = int(self.kwargs['id_espaco'])
        self.id_cliente = int(self.kwargs['id_cliente'])
        try:
            self.vagas = EspacosModel.objects.get(id_espaco=self.id_espaco).vagas
        except AttributeError:
            self.vagas = VAGAS_DEFAULT
        # return getReservasAtuaisMes(self.mes, self.id_espaco)
        return ReservaModel.objects.filter(id_cliente=0)
        # return ReservaModel.objects.filter()

    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(ReservaEventMonthViewset, self).list(request, *args, **kwargs)
        self.start = request.GET.get('start', False)
        print('FULL CALENDAR TESTES')
        print(request.GET.get('format', False))
        print(self.start)
        # reservas = list(response.data)
        # # date = datetime.datetime.today().date()
        # if response.data == []:
        #     return response
        # date = reservas[0]['data_reserva']
        # waiting_another_date = False

        """ response.data = {'event_list':[]} """
        response.data = []
        hoje = datetime.today()
        date = datetime(self.ano, self.mes, hoje.day)
        while date.month == self.mes:
            reservas = ReservaModel.objects.filter(id_espaco=self.id_espaco, data_reserva=date)
            if reservas:
                contem_reserva_do_cliente = False
                for reserva in reservas:
                    if reserva.id_cliente.id_cliente == self.id_cliente:
                        contem_reserva_do_cliente = True
                        break
                if contem_reserva_do_cliente:
                    """ response.data['event_list'].append( {
                    'start': f'{date}T01:00:00',
                    'end': f'{date}T23:00:00',
                    'color': self.COR_RESERVA_USUARIO[0],
                    'textColor': self.COR_RESERVA_USUARIO[1],
                    }) """
                    response.data.append({
                        'start': f'{date.year}-{date.month}-{date.day}T01:00:00',
                        'end': f'{date.year}-{date.month}-{date.day}T23:00:00',
                        'allDay': True,
                        'color': self.COR_RESERVA_USUARIO[0],
                        'textColor': self.COR_RESERVA_USUARIO[1],
                    })
                else:
                    date_dict = getDicionarioReservasDia(id_espaco=self.id_espaco, dia=date, reservas=reservas)
                    porcentagem = getPorcentagemOcupadaDia(date_dict, max_vaga=self.vagas)
                    """ response.data['event_list'].append(getEventoMes(porcentagem, self.CORES_OCUPADO, date)) """
                    response.data.append(getEventoMes(porcentagem, self.CORES_OCUPADO, date))
            date += timedelta(days=1)
        return response

        # def get_evento(date, reservas_do_dia):
        # date_dict = getDicionarioReservasDia(id_espaco=self.id_espaco, dia=date, reservas=reservas_do_dia)
        # porcentagem = getPorcentagemOcupadaDia(date_dict, max_vaga=self.vagas)
        # return getEventoMes(porcentagem, self.CORES_OCUPADO, date)
        """ 
        for i, reserva in enumerate(reservas):
            reserva = dict(reserva)
            if reserva['data_reserva'] != date:
                if reservas_do_dia != []:
                    # date_dict = getDicionarioReservasDia(id_espaco=self.id_espaco, dia=date, reservas=reservas_do_dia)
                    # porcentagem = getPorcentagemOcupadaDia(date_dict, max_vaga=self.vagas)
                    # response.data['event_list'].append(getEventoMes(porcentagem, self.CORES_OCUPADO, date))
                    response.data['event_list'].append(get_evento(date, reservas_do_dia))
                if i == len(reservas)-1 and reserva['id_cliente'] != self.id_cliente:
                    date = reserva['data_reserva']
                    reservas_do_dia.append(reserva)
                    # date_dict = getDicionarioReservasDia(id_espaco=self.id_espaco, dia=date, reservas=reservas_do_dia)
                    # porcentagem = getPorcentagemOcupadaDia(date_dict, max_vaga=self.vagas)
                    # response.data['event_list'].append(getEventoMes(porcentagem, self.CORES_OCUPADO, date))
                    response.data['event_list'].append(get_evento(date, reservas_do_dia))
                    continue
                reservas_do_dia = []

            # if waiting_another_date is False and reserva['data_reserva'] == date:
            if reserva['id_cliente'] == self.id_cliente:
                waiting_another_date = True
                response.data['event_list'].append( {
                # 'title': _('Sem vagas'),
                'start': f'{date}T01:00:00',
                'end': f'{date}T23:00:00',
                'color': self.COR_RESERVA_USUARIO[0],
                'textColor': self.COR_RESERVA_USUARIO[1],
                })
                reservas_do_dia = []
                date = reserva['data_reserva']
                continue
            reservas_do_dia.append(reserva)
            date = reserva['data_reserva']

        """

        # date = datetime.datetime.today().date()
        # while date.month == self.mes+1:
        #     reservas = []
        #     reservas += ReservaModel.objects.filter(id_espaco=self.id_espaco, data_reserva=date)
        #     for reserva in reservas:

        #     date += datetime.timedelta(days=1)
        # for reserva in reservas:

        return response


class ResourceButtonsViewset(generics.ListAPIView):
    serializer_class = serializers.ResouceButtonsSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        self.id_resource_button = self.kwargs['id_resource_button']
        # self.client_id = self.kwargs['client_id']
        # self.lang_code = self.kwargs['lang_code']
        return ResourceButtons.objects.filter(
            # button_tipo=self.id_resource_button,
            # client_id=self.client_id,
            id=self.id_resource_button
        )


class ReservaValidationViewset(generics.ListAPIView):
    serializer_class = serializers.ReservaValidateHashSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        self.id_reserva = self.kwargs['id_reserva']
        self.hash = self.kwargs['hash']
       # self.data_reserva = self.kwargs['data_reserva']
        return ReservaModel.objects.filter(
            id_reserva=self.id_reserva
        )

    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(ReservaValidationViewset, self).list(request, *args, **kwargs)
        lista = response.data
        reserva = {}
        try:
            reserva = lista[0]
        except IndexError:
            response.data = {}
            return response
        if reserva['hash_qrcode'] == self.hash and reserva['data_reserva'] == datetime.now().strftime("%Y-%m-%d"):
            reserva['valido'] = True
            ReservaModel.objects.filter(id_reserva=self.id_reserva).update(hora_entrada_real = datetime.now().strftime("%H:%M:%S"))           
        else:
            reserva['valido'] = False
        response.data = reserva
        return response


class FinalizaReservaViewset(generics.ListAPIView):
    serializer_class = serializers.FinalizarReservaSerializer

    def get_queryset(self):
       
        self.id_reserva = self.kwargs['id_reserva']
        #self.hora_saida_real = self.kwargs['hora_saida_real']
        return ReservaModel.objects.filter(
            id_reserva=self.id_reserva
        )

    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(FinalizaReservaViewset, self).list(request, *args, **kwargs)
        lista = response.data
        reserva = {}
        try:
            reserva = lista[0]
        except IndexError:
            response.data = {'valido':False}
            return response
        if reserva['hora_entrada_real'] is not None:
            reserva['valido'] = True
            ReservaModel.objects.filter(id_reserva=self.id_reserva).update(hora_saida_real = datetime.now().strftime("%H:%M:%S"))           
        else:
            reserva['valido'] = False

        response.data = reserva
        return response

class PagamentoDePlanoAPIView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @staticmethod
    def post(request):
        id_administrador = request.data.pop('id_administrador')
        pagamento = b_pagamento.efetuar_pagamento(request)
        metodo = pagamento.get('payment_type_id')
        cod_mercadopago = pagamento.get('id')
        status_pagamento = pagamento.get('status')
        # administrador = get_administrador_logado_in_cria(request)
        
        erro = pagamento.get('message')
        if not erro:
            Administrador.objects.filter(id=id_administrador).update(plano='Plano Básico', 
                                 validade_plano=datetime.today() + relativedelta(months=+1))
        mensagem_de_erro = erro if erro else 'none'
        return Response(data={'mensagem_de_erro': mensagem_de_erro}, status=status.HTTP_201_CREATED)
