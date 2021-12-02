from django.urls import path, include
from rest_api.router import router
from rest_api.viewsets import *

urlpatterns = [
    path('api_get_by_id/', include(router.urls)),
    path('api/reserva/<data_reserva>/', ReservaDateViewset.as_view()),
    path('api/reserva_by_id/<id_reserva>/', ReservaIdViewset.as_view()),
    path('api/reserva_event/<data_reserva>/<id_cliente>/<id_espaco>/<qtd_reservada>/', ReservaEventDateViewset.as_view()),
    path('api/month_event/<mes>/<id_cliente>/<id_espaco>/', ReservaEventMonthViewset.as_view()),
    path('api/pagamento', PagamentoAPIView.as_view()),
    path('api/pagar_assinatura', PagamentoDePlanoAPIView.as_view()),
    path('api/tipo_espaco/get_preco/<id_tipo_espaco>', TipoEspacoGetPrecoViewset.as_view()),
    path('api/get_resource_button_by_id/<id_resource_button>/', ResourceButtonsViewset.as_view()),
    path('api/validate_reserva/<id_reserva>/<hash>', ReservaValidationViewset.as_view()),
    path('relatorios/api/finaliza_reserva/<id_reserva>', FinalizaReservaViewset.as_view()),
    path('relatorios/api/valida_entrada/<id_reserva>', IniciaReservaViewSet.as_view()),

]