import cria_coworking, sys
from django.shortcuts import render, redirect
import gere_coworking.views.views_helper as h
from cria_coworking.forms import RegistrarAdministradorForm
from domains.models import Domain
from cria_coworking.models import Administrador
from newgen.databases import create_database
import gere_coworking.views.views_manager as m
import gere_coworking.views.businessLayer.cadastro as b_cadastro

from django.core.exceptions import ObjectDoesNotExist

def index(request):
    context = {'turl': h.get_url_without_langcode(request)}
    print('PAAAAAAAARARARARA', file=sys.stderr)
    dominio_id = Domain.objects.using('default').filter(domain=request.domain['domain'])[0].id
    try:
        database = Administrador.objects.using('default').get(domain=dominio_id)
    except ObjectDoesNotExist:
        database = 'default'
        print('DEU EROOOOOOOOOOOOOOOOOOOO', file=sys.stderr)    
    print(request.domain['domain'], file=sys.stderr)
    print('STOP', file=sys.stderr)
    print(dominio_id, file=sys.stderr)
    print(database, file=sys.stderr)
    print('CONTINUEs', file=sys.stderr)
    return render(request, 'cria/index.html', context)

def cadastrar_coworking(request):
    if request.method=='POST':
        form = RegistrarAdministradorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            nome = cd.get('nome')
            create_database(nome)
            return render(request, 'cria/cadastro_novo_coworking.html', {'nome': nome})
    context = {'turl': h.get_url_without_langcode(request),
    'forms': RegistrarAdministradorForm()}
    return render(request, 'cria/cadastro_novo_coworking.html', context)

@m.verificador(cria_coworking=True)
def registrarAdministrador(request, context):
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request, is_administrador=True)
        data['cnpj'] = h.retiraSimbolosString(data['cnpj'])

        administrador = RegistrarAdministradorForm(data)
        data = b_cadastro.configura_banco_e_dominio(data)

        if administrador.is_valid():
            b_cadastro.writeFuncionario(administrador, data, administrador=True)
            return redirect('index')
        
        context['administradorForm'] = administrador
    else:
        context['administradorForm'] = RegistrarAdministradorForm()
        context['administradorForm'].fields["domain"].queryset = Domain.objects.filter(isActive=0)

    return render(request, 'cria/regAdministrator.html', context)