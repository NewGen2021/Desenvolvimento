from domains.models import Domain
from cria_coworking.models import Administrador
from custom_templates.models import InstanceConfig
import json

def get_administrador_by_request(request)-> Administrador:
    domain = request.domain['domain']
    domain = Domain.objects.using('default').get(domain=domain).id
    if domain == 1:
        return None
    return Administrador.objects.using('default').get(domain=domain)

def get_administrador_id_by_domain(domain: str)-> int:
    domain = Domain.objects.using('default').get(domain=domain).id
    return Administrador.objects.using('default').get(domain=domain).id

def get_button_by_request(request) -> str:
    adm_id = get_administrador_id_by_domain(request.domain['domain'])
    return get_button_by_administrador(adm_id)

def get_button_by_administrador(administrador) -> str:
    configs = InstanceConfig.objects.get(client_id=administrador).color_palette
    print('-- config --')
    print(configs)
    button = json.loads(configs.replace("'", "\""))['button']
    return button

def get_button_by_administrador(adm: Administrador) -> str:
    configs = InstanceConfig.objects.get(client_id=adm).color_palette
    print('-- config --')
    print(configs)
    button = json.loads(configs.replace("'", "\""))['button']
    return button

def get_administrador_logado_in_cria(request):
    ''' NÃO USAR FORA DO CRIA COWORKING!'''
    if request.user.is_authenticated:
        usuario = request.user
        cpf_cnpj = usuario.username
        return Administrador.objects.get(cnpj = cpf_cnpj)
    return None