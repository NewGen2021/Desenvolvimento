from django.conf import settings
import mercadopago
sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

def efetuar_pagamento(request):
    # payment_data = {
    #     "transaction_amount": 10.99,
    #     "token": request.POST.get("token"),
    #     "description": "Reserva newgen",
    #     "installments": 1,  # Parcelas
    #     "payment_method_id": "visa",
    #     "payer": {
    #         "email": request.POST.get("email"),
    #         "identification": {
    #             "type": "débito", 
    #             "number": request.POST['numero_cartao']
    #         }
    #     }
    # }
    payment_data = request.data
    payment_response = sdk.payment().create(payment_data)
    return payment_response["response"]
    
