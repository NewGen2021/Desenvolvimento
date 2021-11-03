from rest_framework import serializers
from gere_coworking.models.models import ReservaModel, PagamentoModel, TipoespacoModel

class ReservaSerializer(serializers.ModelSerializer):
    data_reserva = 'batata'
    class Meta:
        model = ReservaModel
        fields = ('id_reserva', 'id_cliente', 'data_reserva', 'hora_entrada', 'hora_saida')

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagamentoModel
        fields = ('metodo', 'cod_mercadopago', 'status_pagamento', 'datahora_log', 'id_reserva')

class TipoEspacoPrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoespacoModel
        fields = ('id_tipoespaco', 'preco')