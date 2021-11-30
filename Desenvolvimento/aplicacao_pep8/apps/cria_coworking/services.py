from django.shortcuts import redirect
import common.selectors as selector
from django.core.management import call_command
import gere_coworking.services.cadastro as b_cadastro
from custom_templates.services import instantiate_template_index, mount_all_customs
from threading import Thread

def getDicionarioAdministradorForm(request) -> dict:
    data = {}
    fields = ["nome", "senha", "cnpj", "email", "telefone", "cep", "logradouro", "numero", "bairro", "estado", "cidade"]
    for field in fields:
        data[field] = request.POST[field]
    return data

def redirect_if_already_has(request):
    adm = selector.get_administrador_logado_in_cria(request)
    if adm:
        if adm.database != None:
            return redirect('gerenciar_plano')
        if adm.plano != None:
            return redirect('registrarCoworking')
    return False

def criar_instancia_nova(data, administrador, context):
    def thread(data, administrador, context):
        data = b_cadastro.configura_banco_e_dominio(data)
        instantiate_template_index(administrador)
        mount_all_customs(administrador, context)
        administrador.database = data['database']
        administrador.save()
        b_cadastro.writeAdministradorInGereCoworking(data=data, banco=data['database'])
        call_command('updatejsondomain')
    Thread(target=thread,args=[data, administrador, context]).start()