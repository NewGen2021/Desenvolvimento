from rest_framework import serializers
from gere_coworking.models import ReservaModel, PagamentoModel, TipoespacoModel
from custom_templates.models import ResourceButtons

class ReservaSerializer(serializers.ModelSerializer):
    data_reserva = 'batata'
    class Meta:
        model = ReservaModel
        fields = ('id_reserva', 'id_cliente', 'data_reserva', 'hora_entrada', 'hora_saida')
    
class ReservaHashSerializer(serializers.ModelSerializer):
    data_reserva = 'batata'
    class Meta:
        model = ReservaModel
        fields = ('id_reserva', 'hash_qrcode', 'id_cliente', 'data_reserva', 'hora_entrada', 'hora_saida')

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagamentoModel
        fields = ('metodo', 'cod_mercadopago', 'status_pagamento', 'datahora_log', 'id_reserva')

class TipoEspacoPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoespacoModel
        fields = ('id_tipoespaco', 'preco', 'compartilhado')

class ResouceButtonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceButtons
        fields = '__all__'

class ReservaValidateHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaModel
        fields = ('id_reserva', 'hash_qrcode','data_reserva')

class FinalizarReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model= ReservaModel
        fields = ('id_reserva', 'hora_saida_real', 'hora_entrada_real')