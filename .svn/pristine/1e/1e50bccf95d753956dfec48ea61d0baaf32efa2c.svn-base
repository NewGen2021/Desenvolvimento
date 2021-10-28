from django.urls import path, include
from rest_api.router import router
from rest_api.viewsets import *

urlpatterns = [
    path('api_get_by_id/', include(router.urls)),
    path('api/reserva/<data_reserva>/', ReservaDateViewset.as_view()),
    path('api/reserva_event/<data_reserva>/<id_cliente>/<id_espaco>/', ReservaEventDateViewset.as_view()),
    path('api/month_event/<mes>/<id_cliente>/<id_espaco>/', ReservaEventMonthViewset.as_view()),
    path('api/pagamento', PagamentoAPIView.as_view())
]