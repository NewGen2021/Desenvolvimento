from django import template
from django.conf import settings
import datetime
import hashlib
import os
import smtplib
import sys
import uuid
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import *
from email.mime.text import MIMEText

from django.contrib.auth.forms import PasswordResetForm
from django.utils.decorators import method_decorator
import gere_coworking.services.cadastro as b_cadastro  # 'b' de 'business"
import gere_coworking.services.config_qrcode as b_qrcode  # 'b' de 'business"
import gere_coworking.services.reserva as b_reserva  # 'b' de 'business"
import qrcode
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetCompleteView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetView
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.utils.translation import get_language, activate
from django.utils.translation import gettext as _
from gere_coworking.forms import *
from gere_coworking.models import *
from gere_coworking.selectors import (get_reservas_cliente, get_reservas_atuais)

import common.selectors as common_selectors
import common.views_manager as m
import common.views_util as h  # 'h' de "helping"


# from django.views.decorators.csrf import csrf_protect


# print("Comentários do console", file=sys.stderr)

# Create your views here.
@m.verificador()
def home(request, context):
    grupo = h.getGrupoDoUsuario(request)
    return render(request, 'gere/template1/cliente/apresentacao/home.html', context)


@m.verificador()
def loginUser(request, context):
    return render(request, 'old/loginUser.html', context)


@m.verificador()
def loginSystem(request, context):
    if request.method == 'GET':
        return render(request, 'gere/template1/cliente/cadastro_e_login/loginSystem.html', context)

    user = h.autenticar(request)
    if user:
        login(request, user)
        if h.isAdministrator(request):
            return redirect('menuAdmin')
        if h.isFuncionario(request):
            return redirect('menuFunc')
        context['grupo'] = h.getGrupoDoUsuario(request)
        # return render(request, 'gere/template1/cliente/apresentacao/index.html', context)
        return redirect('index')

    form = AuthenticationForm(data=request.POST)
    context['form'] = form
    context['mensagem_de_erro'] = h.getFormMensagemErro(form)

    return render(request, 'gere/template1/cliente/cadastro_e_login/loginSystem.html', context)


@m.verificador()
def loginNovo(request, context):
    if request.method == 'POST':
        user = h.autenticar(request)
        if user:
            login(request, user)
            if h.isAdministrator(request):
                return redirect('menuAdmin')
            context['grupo'] = h.getGrupoDoUsuario(request)
            return render(request, 'gere/template1/cliente/apresentacao/index.html', context)

        context['form'] = AuthenticationForm(data=request.POST)
        context['mensagem_de_erro'] = h.getLoginErrors(request)
    else:
        context['form'] = AuthenticationForm()
        context['mensagem_de_erro'] = ''

    return render(request, 'gere/template1/cliente/cadastro_e_login/loginNovo.html', context)


@m.verificador()
def escolherCadastro(request, context):
    return render(request, 'gere/template1/cliente/cadastro_e_login/escolherCadastro.html', context)


# Bruna
@m.verificador()
def base_admin(request, context):
    return render(request, 'gere/template1/base_admin.html', context)


@m.verificador()
def base_funcionario(request, context):
    return render(request, 'gere/template1/base_func.html', context)


@m.verificador()
def registrarUsuario(request, context):
    if request.method == "POST":
        data = b_cadastro.getDicionarioClienteForm(request)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        cliente = ClientePessoaForm(data)
        isPerson = True
        formSelecionado = b_cadastro.getFormSelecionado(request)
        if formSelecionado == "pessoaJuridica":
            cliente = ClienteEmpresaForm(data)
            isPerson = False

        if cliente.is_valid():
            b_cadastro.writeCliente(cliente, data, isPerson)
            return redirect('loginSystem')

        if formSelecionado == "pessoaFisica":
            context['pessoaForm'] = cliente
            context['empresaForm'] = ClienteEmpresaForm
        else:
            context['pessoaForm'] = ClientePessoaForm
            context['empresaForm'] = cliente
        context['selecionado'] = formSelecionado

    else:
        context['pessoaForm'] = ClientePessoaForm
        context['empresaForm'] = ClienteEmpresaForm
        context['selecionado'] = "pessoaFisica"

    return render(request, 'gere/template1/cliente/cadastro_e_login/regUsers.html', context)


@m.verificador()
def registrarFuncionario(request, context):
    if h.isFuncionario(request):
        base_template = "gere/template1/base_func.html"
    elif h.isAdministrator(request):
        base_template = "gere/template1/base_admin.html"
    else:
        base_template = "gere/template1/base.html"
    context["base_template"] = base_template
    
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        funcionario = FuncionariosForm(data)

        if funcionario.is_valid():
            b_cadastro.writeFuncionario(funcionario, data)
            return redirect('loginSystem')

        context['funcionarioForm'] = funcionario
    else:
        context['funcionarioForm'] = FuncionariosForm

    return render(request, 'gere/template1/funcionario/regEmployee.html', context)


@m.verificador()
def registrarAdministrador(request, context):
    if request.method == "POST":
        data = b_cadastro.getDicionarioFuncionarioForm(request, is_administrador=True)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])

        administrador = RegistrarAdministradorForm(data)

        if administrador.is_valid():
            b_cadastro.writeFuncionario(administrador, data, administrador=True)
            return redirect('loginSystem')

        context['administradorForm'] = administrador
    else:
        context['administradorForm'] = RegistrarAdministradorForm

    return render(request, 'cria/regAdministrator.html', context)


@m.verificador()
@login_required
def agendamento(request, context, id_tipo_espaco):
    # Chama as reservas já feitas com uma data futura a hoje de um determinado tipo de espaço

    compartilhado = b_reserva.isCompartilhado(id_tipo_espaco)
    event_list = b_reserva.getEventoReservasCliente(request, id_tipo_espaco)

    reservas = get_reservas_atuais(id_tipo_espaco=id_tipo_espaco)
    dateDicts = b_reserva.getDicionarioReservas(id_tipo_espaco)

    '''Importante'''
    vagas_max = 2

    print('------------- DATE DICTS', file=sys.stderr)
    print(dateDicts, file=sys.stderr)

    event_list = b_reserva.getEventoReservasLotadas(dateDicts, vagas_max, event_list)

    print('------------- EVENT LIST', file=sys.stderr)
    print(event_list, file=sys.stderr)

    hasErrors = False
    error = None

    if request.method == 'POST':
        dicionario = b_reserva.getForm(request, id_tipo_espaco)

        form = ReservaForm(dicionario)
        if form.is_valid():
            hasErrors, error = b_reserva.getFormErrors(dicionario, event_list)
            # Salva o formulário se ele não contiver erros
            if not hasErrors:
                reserva = form.save()
                id_reserva = reserva.id_reserva
                context['token'] = True,
                context['reservas'] = reservas,

                return redirect('pagamento_reserva', id_reserva)
        else:
            error = 'Formulário inválido: '
            for k, v in form.errors.as_json.items():
                error += f'Campo {k} : {v}'

    else:
        form = ReservaForm

    context['cliente_id'] = ClienteModel.objects.get(cpf_cnpj=request.user.username).id_cliente
    # context['eventos'] = event_list
    # print(context['eventos'], file=sys.stderr)
    context['form'] = form
    context['hasErrors'] = hasErrors
    context['error'] = error
    context['compartilhado'] = compartilhado
    
    ITENS_POR_PAGINA: int = 3
    espacos = EspacosModel.objects.filter(id_tipo_espaco=id_tipo_espaco)
    p = Paginator(espacos.order_by('preco'), ITENS_POR_PAGINA)
    pages = []
    for i in range(p.num_pages):
        page = p.page(i + 1)
        page.num_items = len(page.object_list)
        pages.append(page)
    context['pages'] = pages
    context['tipo_espaco'] = EspacosModel.objects.filter(id_tipo_espaco=1)[0]
    
    return render(request, 'gere/template1/cliente/agendamento/reserva2Calendario.html', context)


@m.verificador()
def assinatura(request, context):
    return render(request, 'gere/template1/cliente/apresentacao/assinatura.html', context)


# @csrf_protect
@m.verificador()
def index(request, context):
    id_adm = common_selectors.get_administrador_by_request(request).id
    # return render(request, 'gere/template1/cliente/apresentacao/index.html', context)
    return render(request, f'instances/{id_adm}/cliente/apresentacao/index.html', context)


@m.verificador()
def reserva(request, context):
    ITENS_POR_PAGINA: int = 3
    tipo_espacos = TipoespacoModel.objects.all()
    # tipo_espacos_validos =
    for tipo_espaco in tipo_espacos:
        num = EspacosModel.objects.filter(id_tipo_espaco=tipo_espaco, status_espaco=1).count()
        if num == 0:
            tipo_espacos = tipo_espacos.exclude(id_tipoespaco=tipo_espaco.id_tipoespaco)
    p = Paginator(tipo_espacos.order_by('nome'), ITENS_POR_PAGINA)
    pages = []
    for i in range(p.num_pages):
        pages.append(p.page(i + 1))
    context['pages'] = pages
    # context['imagem'] = TipoespacoModel.objects.get(id_tipoespaco=1).imagem
    # context['url_imagem'] = TipoespacoModel.objects.get(id_tipoespaco=1).imagem.decode('utf-8')
    return render(request, 'gere/template1/cliente/agendamento/reserva1EscolherEspaco.html', context)


@m.verificador()
def listarReservas(request, context):
    reservas = get_reservas_cliente(cpf_cnpj=request.user.username)
    context['reservas'] = reservas
    return render(request, 'gere/template1/cliente/agendamento/listarReservas.html', context)


@m.verificador()
def listarReservasIndex(request, context):
    reservas = get_reservas_cliente(cpf_cnpj=request.user.username)
    eventos = b_reserva.getEventoReservasCliente(request, 0)
    context['reservas'] = reservas
    context['eventos'] = eventos
    context['ja_reservado_mensagem'] = _('Sua reserva está marcada para dia ')

    return render(request, 'gere/template1/cliente/agendamento/listarReservasIndex.html', context)


################################## EQUIPAMENTOS / MATERIAIS ####################################

@m.verificador()
def reserva_de_equipamentos(request, context):
    ITENS_POR_PAGINA: int = 3
    tipo_equipamento = EquipamentosModel.objects.all()
    # tipo_espacos_validos =
    for tipo_espaco in tipo_equipamento:
        num = EquipamentosModel.objects.filter(id_equipamento=tipo_equipamento, status_equipamento=1).count()
        if num == 0:
            tipo_equipamento = tipo_equipamento.exclude(id_tipoequipamento=tipo_equipamento.id_tipoequipamento)
    p = Paginator(tipo_equipamento, ITENS_POR_PAGINA)
    pages = []
    for i in range(p.num_pages):
        pages.append(p.page(i + 1))
    context['pages'] = pages
    context['imagem'] = EquipamentosModel.objects.get(id_tipoequipamento=1).imagem
    context['url_imagem'] = EquipamentosModel.objects.get(id_tipoequipamento=1).imagem.decode('utf-8')
    return render(request, 'gere/template1/cliente/agendamento/reserva1EscolherEquipamento.html', context)


@m.verificador()
def listarEquipamentos(request, context):
    reserva_equipamento = EquipamentoreservaModel.objects.get_reservas_cliente(cpf_cnpj=request.user.username)
    context['reserva_equipamentos'] = reserva_equipamento
    return render(request, 'gere/template1/cliente/agendamento/listarReservasEquipamentos.html', context)


@m.verificador()
def listarReservasEquipamentosIndex(request, context):
    reservas = EquipamentoreservaModel.objects.get_reservas_cliente(cpf_cnpj=request.user.username)
    eventos = b_reserva.getEventoReservasCliente(request, 0)
    context['reservas'] = reservas
    context['eventos'] = eventos
    context['ja_reservado_mensagem'] = _('Sua reserva está marcada para dia ')

    return render(request, 'gere/template1/cliente/agendamento/listarReservasEquipamentosIndex.html', context)


##################################################################################################

@m.verificador()
def menuAdmin(request, context):
    return render(request, 'gere/template1/adm/menuAdmin.html', context)
    if h.isAdministrator(request):
        return render(request, 'gere/template1/adm/menuAdmin.html', context)
    return render(request, 'gere/template1/cliente/apresentacao/index.html', context)


@m.verificador()
def menuFunc(request, context):
    return render(request, 'gere/template1/funcionario/menuFuncionario.html', context)


@m.verificador()
def customizacao(request, context):
    return render(request, 'gere/template1/adm/customizacao.html', context)


@m.verificador()
def emProducao(request, context):
    return render(request, 'erros/emProducao.html', context)


@m.verificador()
def base_html(request, context):
    return render(request, 'gere/template1/base.html', context)


@m.verificador()
def teste(request, context):
    hostname = request.get_host().split(':')[0].lower()
    context['mundo'] = _('mundo')
    # ReservaModel.objects.filter(id_reserva=1).update(hash_qrcode="67101e2955c993ea6f3a0ae8e70c1502")
    # reserva = ReservaModel.objects.get(id_reserva=1)
    # user = User.objects.get_or_create(username="30426238000144", password="senha", email="x.gabriel12@gmail")
    # user = User.objects.get(username="30426238000144")
    # cliente = ClienteModel.objects.create(nome="JoJo Company",
    #  cpf_cnpj="30426238000144", email="x.gabriel12@gmail", telefone="(11) 977866159",
    #  logradouro="João Brícola", numero="981", bairro="Centro", cidade="São Paulo", estado="SP", user=user)
    # user = User.objects.create_user(username="58529850000161", password="senha", email="bruna_rodriguesoliver@hotmail.com", first_name="Bruna",
    #      last_name="Rodrigues", is_superuser=True, is_staff=True)
    # user = User.objects.get(username="58529850000161")
    # b_cadastro.configuraGrupoUsuario(user, tipo='administrador')
    # funcionario = FuncionariosModel.objects.create(nome="Bruna",
    #  cpf_cnpj="58529850000161", email="bruna_rodriguesoliver@hotmail.com", telefone="(11) 977866159", data_nascimento="2000-08-28",
    #  logradouro="João Brícola", numero="981", bairro="Centro", cidade="São Paulo", estado="SP", user=user)
    # if reserva.is_aluguel:
    #     context['fruta'] = _('É aluguel')
    # else:
    #     context['fruta'] = _('Falso, não é aluguel.')
    # context['fruta'] = funcionario.nome
    context['codigo'] = 'pix'
    context['actual_host'] = hostname
    # context['domain'] = request.domain
    context['d'] = request.domain
    context['tenant_name'] = hostname.split('.')[0]
    return render(request, 'gere/template1/cliente/apresentacao/teste.html', context)


def translate(language):
    cur_language = get_language()
    try:
        activate(language)
        text = _('WORLD')
    finally:
        activate(cur_language)
    return text


@m.verificador()
def form_teste(request, context):
    if request.method == "POST":
        pagamento = FormTesteForm(request.POST)  # Pega os dados do formulário e joga em um objeto de form pagamento

        if pagamento.is_valid():  # vê se o pagamento é válido
            id = int(
                request.POST['id_reserva'])  # pega do dicionário request.POST o campo id_reserva e converte em inteiro
            reserva = ReservaModel.objects.get(id_reserva=id)  # pega uma reserva com o id especifico

            PagamentoModel.objects.create(  # cria um model de pagamento no banco de dados
                metodo=request.POST['metodo'],
                cod_mercadopago=request.POST['cod_mercadopago'],
                status_pagamento=request.POST['status_pagamento'],
                datahora_log=datetime.datetime.now(),
                id_reserva=reserva,
            )
            return redirect('index')  # redireciona para o início
        context['form'] = pagamento  # pega o formulário com erro e manda para o context caso o formulário seja inválido
    else:
        context['form'] = FormTesteForm  # pega um formulário novo para mostrar pro usuário, caso seja com o método get

    return render(request, 'gere/template1/cliente/apresentacao/teste_form.html', context)  # imprime a tela pro usuário


@m.verificador()
def form_teste2(request, context):
    if request.method == "POST":  # se for com o método post (quando o usuário clicar em enviar)
        form = FormTeste2Form(request.POST)  # preenche o formulário com os dados do dicionário request.POST
        if form.is_valid():  # confere se o formulário é válido
            context['resultado'] = request.POST[
                'numero_cartao']  # pega o campo "numero_cartao" do dicionário request.POST e manda para o context para mostrar na tela
        context[
            'form'] = form  # se o formulário for inválido, pega o formulário preenchido com os erros e mostra pro usuário
    else:
        context['form'] = FormTeste2Form  # se o método for get, pega o formulário novo sem ser preenchido

    return render(request, 'gere/template1/cliente/apresentacao/teste_form.html', context)  # imprime a tela pro usuário


@m.verificador()
def form_pagamento(request, context, id_reserva):
    reserva = ReservaModel.objects.get(id_reserva=id_reserva)
    context['valor_compra'] = "%.2f" % float(reserva.preco_total)
    context['valor_compra10'] = "%.2f" % float(reserva.preco_total) / 10
    aluguel = reserva.is_aluguel

    if request.method == "POST":
        form = FormPagamento(request.POST)
        mensagem_de_erro = request.POST['mensagem_de_erro']
        print(mensagem_de_erro)
        print(request.POST)
        if mensagem_de_erro == '' or mensagem_de_erro == 'none':
            return redirect('listarReservas')
        else:
            context['form'] = form
        if aluguel == 1:
            gerar_qrcode()

    else:
        context['form'] = FormPagamento
    context['id_reserva'] = id_reserva

    return render(request, 'gere/template1/cliente/pagamento/pagamento2.html', context)  # imprime a tela pro usuário


@m.verificador()
def form_pagamento_teste(request, context):
    return render(request, 'gere/template1/cliente/pagamento/pagamento.html', context)  # imprime a tela pro usuário


# Bruna - início sessão de reset de senha
class CustomPasswordResetView(PasswordResetView):
    pass

class CustomPasswordResetDoneView(PasswordResetDoneView):
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordResetForm
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Redefinição de senha concluida')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        context['login_newgen'] = 'login.html'
        context['login_system'] = 'loginSystem.html'
        context['isNewgen'] = False
        request = self.request
        context['turl'] = h.get_url_without_langcode(request)
        context['domain'] = str(request.domain['domain'])
        return context

# fim sessão reset de senha

@m.verificador()
def listar_espacos(request, context):
    if h.isFuncionario(request):
        base_template = "gere/template1/base_func.html"
    elif h.isAdministrator(request):
        base_template = "gere/template1/base_admin.html"
    else:
        base_template = "gere/template1/base.html"
    context["base_template"] = base_template

    espaco = request.GET.get('espaco', False)  # Lógica de averiguar se é espaço ou tipo espaço
    if espaco:
        items = EspacosModel.objects.all().order_by('id_tipo_espaco')
    else:
        items = TipoespacoModel.objects.all()
    # item = items[0]
    # items = []
    # for i in range(100):
    #     items.append(item)
    p = Paginator(items, 6)
    page_num = request.GET.get('page', 1)  # Pega o número da página caso não exista, retorna 1

    try:  # Se a página não existir, faz a página voltar para a 1
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context['items'] = page
    context['page_num'] = page_num
    context['number_of_pages'] = p.num_pages
    context['is_tipo_espaco'] = "false" if espaco else "true"
    context['is_espaco'] = "true" if espaco else "false"
    context['active_tipo_espaco'] = None if espaco else "active"
    context['active_espaco'] = "active" if espaco else None
    context['opcao'] = "espaco" if espaco else "tipo_espaco"

    return render(request, 'gere/template1/adm/espacos/listar_espacos.html', context)


@m.verificador()
def editar_tipo_espaco(request, context, id_tipo_espaco):
    try:
        tipo_espaco = TipoespacoModel.objects.get(id_tipoespaco=id_tipo_espaco)
    except TipoespacoModel.DoesNotExist:
        context['nao_existe'] = True
        return render(request, 'gere/template1/adm/espacos/editar_tipo_espaco.html', context)
    if request.method == "POST":
        if request.FILES:  # Verifica se o usuário upou um arquivo
            form = TipoespacoForm(request.POST, request.FILES, instance=tipo_espaco)
            if form.is_valid():
                form.save()
                return redirect("listar_espacos")
        else:
            form = TipoespacoForm(request.POST, instance=tipo_espaco)
            if form.is_valid():
                TipoespacoModel.objects.filter(id_tipoespaco=id_tipo_espaco).update(
                    nome=form.cleaned_data['nome'],
                    compartilhado=form.cleaned_data['compartilhado'],
                    descricao=form.cleaned_data['descricao'],
                    tempo_limpeza=form.cleaned_data['tempo_limpeza'],
                    preco=form.cleaned_data['preco'],
                )
                return redirect("listar_espacos")
        context['form'] = form
    else:
        tipo_espaco = TipoespacoModel.objects.get(id_tipoespaco=id_tipo_espaco)
        form = TipoespacoForm(instance=tipo_espaco)
        context['form'] = form
    tipo_espaco = TipoespacoModel.objects.get(id_tipoespaco=id_tipo_espaco)
    if tipo_espaco.imagem:
        context['imagem'] = tipo_espaco.imagem.decode('utf-8')
    context['compartilhado'] = tipo_espaco.compartilhado

    return render(request, 'gere/template1/adm/espacos/editar_tipo_espaco.html', context)


@m.verificador()
def editar_espaco(request, context, id_espaco):
    try:
        espaco = EspacosModel.objects.get(id_espaco=id_espaco)
    except EspacosModel.DoesNotExist:
        context['nao_existe'] = True
        return render(request, 'gere/template1/adm/espacos/editar_espaco.html', context)
    if request.method == "POST":
        # form = EspacosForm(request.POST, request.FILES, instance=espaco)
        if request.POST['preco'] is None:
            request.POST['preco'] = EspacosModel.objects.get(id_espaco=id_espaco).id_tipo_espaco.preco
        if request.FILES:  # Verifica se o usuário upou um arquivo
            form = EspacosForm(request.POST, request.FILES, instance=espaco)
            if form.is_valid():
                form.save()
                return redirect(reverse('listar_espacos') + "?espaco=1")
        else:
            form = EspacosForm(request.POST, instance=espaco)
            if form.is_valid():
                EspacosModel.objects.filter(id_espaco=id_espaco).update(
                    id_tipo_espaco=form.cleaned_data['id_tipo_espaco'],
                    vagas=form.cleaned_data['vagas'],
                    preco=form.cleaned_data['preco'],
                    status_espaco=form.cleaned_data['status_espaco'],
                )
                return redirect(reverse('listar_espacos') + "?espaco=1")
        context['form'] = form
    else:
        espaco = EspacosModel.objects.get(id_espaco=id_espaco)
        form = EspacosForm(instance=espaco)
        context['form'] = form
    espaco = EspacosModel.objects.get(id_espaco=id_espaco)

    if espaco.imagem:
        context['imagem'] = espaco.imagem.decode('utf-8')
    context['compartilhado'] = espaco.id_tipo_espaco.compartilhado
    context['preco'] = "%.2f" % (espaco.preco if espaco.preco else espaco.id_tipo_espaco.preco)
    context['preco_padrao'] = _("O preço padrão para %s é R$%s." % (espaco.id_tipo_espaco.nome, context['preco']))

    print(context['form'])

    return render(request, 'gere/template1/adm/espacos/editar_espaco.html', context)


@m.verificador()
def criar_tipo_espaco(request, context):
    if request.method == "POST":
        nome = request.POST.get('nome')
        count = TipoespacoModel.objects.filter(nome=nome).count()
        if count > 0:
            messages.error(request, _('Tipo de espaço já cadastrado com este Nome !'))
            return redirect('criar_tipo_espaco')
        else:
            form = TipoespacoLabelsForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('listar_espacos')
    else:
        context['form'] = TipoespacoLabelsForm
        return render(request, 'gere/template1/adm/espacos/criar_tipo_espaco.html', context)


@m.verificador()
def criar_espaco(request, context):
    if request.method == "POST":
        form = EspacosLabelsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('listar_espacos') + "?espaco=1")
    else:
        context['form'] = EspacosLabelsForm
        context['existe_tipos_espacos'] = TipoespacoModel.objects.count()
        return render(request, 'gere/template1/adm/espacos/criar_espaco.html', context)


@m.verificador()
def excluir_tipo_espaco(request, context, id_tipo_espaco):
    tipo_espaco = TipoespacoModel.objects.get(id_tipoespaco=id_tipo_espaco)
    nome = tipo_espaco.nome
    tipo_espaco.delete()
    messages.success(request, _('Tipo de espaço "%s" excluído com sucesso !' % nome))
    return redirect('listar_espacos')


@m.verificador()
def excluir_espaco(request, context, id_espaco):
    espaco = EspacosModel.objects.get(id_espaco=id_espaco)
    nome = str(espaco)
    espaco.delete()
    messages.success(request, _('Espaço "%s" excluído com sucesso !' % nome))
    return redirect(reverse('listar_espacos') + "?espaco=1")


@m.verificador()
def testarLayout(request, context):
    return render(request, 'old/testarLayout.html', context)


@m.verificador()
def testarLayout2(request, context):
    return render(request, 'old/testarLayout2.html', context)


# Bruna - desenvolvendo envio de qrcode
@m.verificador()
def gerar_qrcode(request, context, id_reserva):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    chave_aleatoria = str(uuid.uuid4())
    cod_do_qr = f'{id_reserva}//{chave_aleatoria}'
    hash = hashlib.md5(cod_do_qr.encode('utf-8')).hexdigest()
    qr.add_data(f'{id_reserva}//{hash}')
    qr.make(fit=True)
    b_qrcode.salvar_no_banco(hash, id_reserva)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f'static/media/qrcode{id_reserva}.png')

    #email = request.user.email
    email = 'brunaoliveiraweb@gmail.com'
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    login = settings.EMAIL_HOST_USER
    senha = settings.EMAIL_HOST_PASSWORD

    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(login, senha)

    corpo = "Use este QRcode para confirmar sua reserva no momento da entrada no estabelecimento."

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = email
    email_msg['Subject'] = "Qrcode para validação de entrada"
    email_msg.attach(MIMEText(corpo, "html"))

    caminhoArquivo = f"static/media/qrcode{id_reserva}.png"
    attachment = open(caminhoArquivo, 'rb')

    att = MIMEBase('application', 'octed-stream')
    att.set_payload(attachment.read())
    encoders.encode_base64(att)

    att.add_header('Content-Disposition', f'attachment; filename=qrcode.png')
    attachment.close()

    email_msg.attach(att)

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

    os.remove(f"static/media/qrcode{id_reserva}.png")

    return render(request, 'gere/template1/cliente/pagamento/qrcode_envio.html', context)


# Bruna - desenvolvendo leitor de qrode
@m.verificador()
def leitor_qrcode(request, context):
    return render(request, 'gere/template1/funcionario/leitor_qrcode.html', context)


@m.verificador()
def testando_qrcode(request, context):
    return render(request, 'old/qrcode2.html', context)


# Beatriz - Transferência de responsabilidade
@m.verificador()
def transfereTitular(request, context):
    email = request.user.email
    host = "smtp.gmail.com"
    port = "587"
    login = "newgenoficial2021@gmail.com"
    senha = "jchxwrmlxaypxgei"

    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(login, senha)

    corpo = "Você recebeu um pedido de transferência de titularidade. Por favor, clique no link abaixo para aceitar ou recusar."

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = email
    email_msg['Subject'] = "Pedido de Transferência de Titularidade"
    email_msg.attach(MIMEText(corpo, "html"))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

    return render(request, 'gere/template1/cliente/pagamento/transfere_titular_envio.html', context)

    return render(request, 'gere/template1/cliente/pagamento/transfere_titular_erro.html', context)


@m.verificador()
def transfereTitularEnvio(request, context):
    pass


@m.verificador()
def transfereTitularErro(request, context):
    pass

####Tentativa de relatorio - Brunaa ###
from django.views.generic.list import ListView
from dateutil.parser import parse
from datetime import timedelta


class ReservaList(ListView):

    #method_decorator(m.verificador)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = ReservaModel
    template_name = 'gere/template1/relatorios/reservas.html'
    
    
    def get_queryset(self):
        queryset = ReservaModel.objects.all()
        #queryset = ReservaModel.objects.filter(data_reserva = datetime.date.today().strftime("%Y-%m-%d"))
        #queryset = ReservaModel.objects.filter(data_reserva = datetime.date.today().strftime("%Y-%m-%d"), hora_saida_real = None).exclude(hora_entrada_real = None).order_by('hora_saida')

        return queryset

@m.verificador()
def finalizaReserva(request,context, self):
    ReservaModel.objects.filter(id_reserva=self.id_reserva).update(hora_saida_real = datetime.now().strftime("%H:%M:%S"))           
    
    return render(request, 'gere/template1/relatorios/reservas.html', context)
   
class PagamentoList(ListView):
    model = PagamentoModel 
    template_name= 'gere/template1/relatorios/pagamentos.html'

@m.verificador()
def advertencia(request, context):
    return render(request, 'gere/template1/funcionario/advertencia.html', context)


@m.verificador()
def testar_bootstrap(request, context):
    
    ITENS_POR_PAGINA: int = 3
    # tipo_espacos = EspacosModel.objects.filter(id_tipo_espaco=1)
    tipo_espacos = EspacosModel.objects.all()
    p = Paginator(tipo_espacos.order_by('preco'), ITENS_POR_PAGINA)
    # p.page(2).object_list
    pages = []
    # p.page(1).end_index
    p.page(1).__len__
    for i in range(p.num_pages):
        page = p.page(i + 1)
        page.num_items = len(page.object_list)
        pages.append(page)
    context['pages'] = pages
    context['tipo_espaco'] = EspacosModel.objects.filter(id_tipo_espaco=1)[0]
    # context['imagem'] = TipoespacoModel.objects.get(id_tipoespaco=1).imagem
    # context['url_imagem'] = TipoespacoModel.objects.get(id_tipoespaco=1).imagem.decode('utf-8')
    
    return render(request, 'gere/template1/cliente/apresentacao/teste2.html', context)