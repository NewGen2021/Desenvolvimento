from django.shortcuts import render
import gere_coworking.views.views_helper as h
from cria_coworking.forms import RegistrarAdministradorForm
from newgen.databases import create_database

def apresentacao(request):
    context = {'turl': h.get_url_without_langcode(request)}
    return render(request, 'criacaoCoworking/apresentacao.html', context)

def cadastrar_coworking(request):
    if request.method=='POST':
        form = RegistrarAdministradorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            nome = cd.get('nome')
            create_database(nome)
            return render(request, 'criacaoCoworking/cadastro_novo_coworking.html', {'nome': nome})
    context = {'turl': h.get_url_without_langcode(request),
    'forms': RegistrarAdministradorForm()}
    return render(request, 'criacaoCoworking/cadastro_novo_coworking.html', context)
