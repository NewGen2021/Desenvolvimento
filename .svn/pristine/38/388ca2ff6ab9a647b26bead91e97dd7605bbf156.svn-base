from gere_coworking.models.models import *
from django.core.mail import send_mail
import qrcode


def salvar_no_banco(hash_qrcode, id_reserva):
    ReservaModel.objects.filter(id_reserva=id_reserva).update(hash_qrcode=hash_qrcode)
    
