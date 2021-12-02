from cria_coworking.models import *


def get_current_adm_by_request(request) -> Administrador:
    domain = Domain.objects.using('default').get(domain=request.domain['domain'])
    return Administrador.objects.using('default').get(domain=domain)
