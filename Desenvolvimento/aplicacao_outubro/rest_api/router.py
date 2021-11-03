from . import viewsets
from rest_framework import routers

router = routers.DefaultRouter()
router.register('reserva', viewsets.BasicReservaViewset)

# localhost:p/api/reserva/1
# GET, POST, UPDATE, DELETE
# list, retrieve