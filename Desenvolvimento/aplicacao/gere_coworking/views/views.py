from django.conf import settings
from django.core.files import File as DjangoFile
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User, UserManager
from django.urls import reverse
from django.contrib.auth.forms import  UserCreationForm, UsernameField
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth import get_user
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate
from django.core.paginator import EmptyPage, Paginator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect


from django.template.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect

from crispy_forms.utils import render_crispy_form
from django.views.generic.edit import FormView

from newgen.settings import BASE_DIR
from gere_coworking.forms.forms import *
from gere_coworking.models.models import *
import gere_coworking.views.views_helper as h    # 'h' de "helping"
import gere_coworking.views.businessLayer.cadastro as b_cadastro   # 'b' de 'business"
import gere_coworking.views.businessLayer.reserva as b_reserva   # 'b' de 'business"
import gere_coworking.views.businessLayer.pagamento as b_pagamento   # 'b' de 'business"
import gere_coworking.views.views_manager as m


import os
import datetime, sys

#print("Comentários do console", file=sys.stderr)

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
        context['grupo'] = h.getGrupoDoUsuario(request)
        return render(request, 'gere/template1/cliente/apresentacao/index.html', context)


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

    reservas = ReservaModel.objects.get_reservas_atuais(id_tipo_espaco = id_tipo_espaco)
    dateDicts = b_reserva.getDicionarioReservas(id_tipo_espaco)
    
    '''Importante'''
    vagas_max = 2

    print('------------- DATE DICTS', file=sys.stderr)
    print(dateDicts, file=sys.stderr)

    event_list = b_reserva.getEventoReservasLotadas(dateDicts, vagas_max, event_list)
    
    # print('------------- EVENT LIST', file=sys.stderr)
    # print(event_list, file=sys.stderr)

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

    context['eventos'] = event_list
    print(context['eventos'], file=sys.stderr)
    context['form'] = form
    context['hasErrors'] = hasErrors
    context['error'] = error
    context['compartilhado'] = compartilhado

    return render(request, 'gere/template1/cliente/agendamento/reserva2Calendario.html', context)

@m.verificador()
def assinatura(request, context):
    return render(request, 'gere/template1/cliente/apresentacao/assinatura.html', context)

#@csrf_protect
@m.verificador()
def index(request, context):    
    return render(request, 'gere/template1/cliente/apresentacao/index.html', context)

@m.verificador()
def reserva(request, context):
    return render(request, 'gere/template1/cliente/agendamento/reserva1EscolherEspaco.html', context)

@m.verificador()
def listarReservas(request, context):
    reservas = ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username)
    context['reservas'] = reservas
    return render(request, 'gere/template1/cliente/agendamento/listarReservas.html', context)

@m.verificador()
def listarReservasIndex(request, context):

    reservas = ReservaModel.objects.get_reservas_cliente(cpf_cnpj = request.user.username)
    eventos = b_reserva.getEventoReservasCliente(request, 0)
    context['reservas'] = reservas
    context['eventos'] = eventos
    context['ja_reservado_mensagem'] = _('Sua reserva está marcada para dia ')

    return render(request, 'gere/template1/cliente/agendamento/listarReservasIndex.html', context)

@m.verificador()
def menuAdmin(request, context):
    return render(request, 'gere/template1/adm/menuAdmin.html', context)
    if h.isAdministrator(request):
        return render(request, 'gere/template1/adm/menuAdmin.html', context)
    return render(request, 'gere/template1/cliente/apresentacao/index.html', context)
    

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
            id = int(request.POST['id_reserva'])    # pega do dicionário request.POST o campo id_reserva e converte em inteiro
            reserva = ReservaModel.objects.get(id_reserva=id)  # pega uma reserva com o id especifico

            PagamentoModel.objects.create(  # cria um model de pagamento no banco de dados
                metodo = request.POST['metodo'],
                cod_mercadopago = request.POST['cod_mercadopago'],
                status_pagamento = request.POST['status_pagamento'],
                datahora_log = datetime.datetime.now(),
                id_reserva = reserva,
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
            context['resultado'] = request.POST['numero_cartao']  # pega o campo "numero_cartao" do dicionário request.POST e manda para o context para mostrar na tela
        context['form'] = form  # se o formulário for inválido, pega o formulário preenchido com os erros e mostra pro usuário
    else:
        context['form'] = FormTeste2Form  # se o método for get, pega o formulário novo sem ser preenchido

    return render(request, 'gere/template1/cliente/apresentacao/teste_form.html', context)  # imprime a tela pro usuário

@m.verificador()
def form_pagamento(request, context, id_reserva):
    if request.method == "POST":
        form = FormPagamento(request.POST)
        mensagem_de_erro = request.POST['mensagem_de_erro']
        print('BATATA QUENTEEEEEEEEEEEEEEEEE')
        print(mensagem_de_erro)
        print(request.POST)
        if mensagem_de_erro == '' or mensagem_de_erro == 'none':
            return redirect('listarReservas')
        else:
            # form.is_valid()
            # data = form.data
            # form_novo = FormPagamento(data=data)
            # form_novo.add_error(field=None, error=mensagem_de_erro)
            context['form'] = form
    else:
        context['form'] = FormPagamento
    context['id_reserva'] = id_reserva

    return render(request, 'gere/template1/cliente/pagamento/pagamento2.html', context)  # imprime a tela pro usuário

@m.verificador()
def form_pagamento_teste(request, context):
    return render(request, 'gere/template1/cliente/pagamento/pagamento.html', context)  # imprime a tela pro usuário

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        context['login_newgen'] = 'login.html'
        context['login_system'] = 'loginSystem.html'
        context['isNewgen'] = False
        request = self.request
        context['turl'] = h.get_url_without_langcode(request)
        context['domain']= str(request.domain['domain'])
        return context

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass

class CustomPasswordResetDoneView(PasswordResetDoneView):
    pass

class CustomPasswordResetView(PasswordResetView):
     form_class = CustomPasswordResetForm

@m.verificador()
def listar_espacos(request, context):
    espaco = request.GET.get('espaco', False)   # Lógica de averiguar se é espaço ou tipo espaço
    if espaco:
        items = EspacosModel.objects.all().order_by('id_tipo_espaco')
    else:
        items = TipoespacoModel.objects.all()
    # item = items[0]
    # items = []
    # for i in range(100):
    #     items.append(item)
    p = Paginator(items, 20)
    page_num = request.GET.get('page', 1)   # Pega o número da página caso não exista, retorna 1
    
    try:    # Se a página não existir, faz a página voltar para a 1
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

    return render(request, 'gere/template1/adm/espacos/listar_espacos.html', context)

@m.verificador()
def editar_tipo_espaco(request, context, id_tipo_espaco):
    try:
        tipo_espaco = TipoespacoModel.objects.get(id_tipoespaco=id_tipo_espaco)
    except TipoespacoModel.DoesNotExist:
        context['nao_existe'] = True
        return render(request, 'gere/template1/adm/espacos/editar_tipo_espaco.html', context)
    if request.method == "POST":
        form = TipoespacoForm(request.POST, request.FILES, instance=tipo_espaco)
        # if request.FILES:
        #     form = TipoespacoForm(request.POST, request.FILES, instance=tipo_espaco)
        #     print('SAFADO ENTROU AQUI')
        # else:
        #     form = TipoespacoForm(request.POST, instance=tipo_espaco)
        #     print('TÁ SAFE')
        if form.is_valid():
            print('OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
            print(form.cleaned_data)
            # print(form.cleaned_data['imagem'])
            # if form.cleaned_data['imagem'] == '':
            tipoesp = form.save(commit=False)
            data = {
                'descricao': tipoesp.descricao,
                'nome': tipoesp.nome,
                'preco': tipoesp.preco,
                'compartilhado': tipoesp.compartilhado,
                'tempo_limpeza': tipoesp.tempo_limpeza,
                # 'imagem': DjangoFile(open(tipoesp.imagem.path, mode='rb'), name=tipoesp.imagem.path)
                'imagem': tipoesp.imagem.decode('utf-8')
            }
            form = TipoespacoForm(data=data, instance=tipo_espaco)
            # # data['imagem'] = tipo_espaco.imagem
            # # data['imagem'] = DjangoFile(open(tipo_espaco.imagem, mode='rb'), name=tipo_espaco.imagem)
            form.save()
            # else:
            # form.save()
            return redirect("listar_espacos")
        else:
            context['tipo_espaco_form'] = form
    else:
        tipo_espaco = TipoespacoModel.objects.get(id_tipoespaco=id_tipo_espaco)
        data = {
                'descricao': tipo_espaco.descricao,
                'nome': tipo_espaco.nome,
                'preco': tipo_espaco.preco,
                'compartilhado': tipo_espaco.compartilhado,
                'tempo_limpeza': tipo_espaco.tempo_limpeza,
                'imagem': tipo_espaco.imagem,
            }
        print('IMAGEMEPAOSKADPOKSDAPOS')
        print(tipo_espaco)
        print(tipo_espaco.imagem)
        # print(form)
        form = TipoespacoForm(instance=tipo_espaco)
        context['tipo_espaco_form'] = form
        context['imagem'] = tipo_espaco.imagem.decode('utf-8')

    return render(request, 'gere/template1/adm/espacos/editar_tipo_espaco.html', context)
