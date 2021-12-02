from gere_coworking.models import ReservaModel, ClienteModel
from django.core.mail import send_mail


# Atualiza o Id_Cliente presente na tabela de Reservas, e garante a normalização da Foreign Key

def transfSalvarNoBanco(id_cliente, id_reserva):
    reserva = ReservaModel.objects.get(id_reserva=id_reserva)
    novoTitular = ClienteModel.objects.get(id_cliente=id_cliente)
    reserva.id_cliente = novoTitular
    reserva.save()
