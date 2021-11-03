''' 
    * PARA ARMAZENAR CÓDIGOS LEGADOS COMENTADOS,
    * OBS: ESTE DOCUMENTO NÃO TEM FUNÇÃO NENHUMA DENTRO DO CÓDIGO
'''

# forms.py

""" from input_mask.widgets import InputMask
from django_localflavor_br.forms import BRCPFField, BRPhoneNumberField
from input_mask.contrib.localflavor.br.widgets import BRCPFInput, BRPhoneNumberInput """


""" class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2'] """

""" class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="cpf/cnpj")
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))

    class Meta:
        model = User
        fields = ['username', 'password'] """

""" class ClienteEmpresaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="Nome Social")
    # cpf = BRCPFField(widget= BRCPFInput(
    #         attrs={'class': 'form-control','data-mask': '000.000.000-00', 'required': 'true'}), label="CPF")
    # data_nascimento = forms.DateField(widget=DataCustomInput(
    #         attrs={'class': 'form-control', 'data-mask': '00/00/0000', 'required': 'true'}), label="Data de Nascimento")
    # telefone = forms.(widget=BRPhoneNumberInput(
    #         attrs={'class': 'form-control', 'data-mask': '(00) 00000-0000', 'required': 'true'}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label="CNPJ")
    logradouro = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    estado = forms.Select(
        attrs={'required': 'true'})
    # numero = forms.IntegerField(widget=forms.TextInput(
    #         attrs={'required': 'true'}))
    cidade = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={'required': 'true'}))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000"}))

    class Meta:
        model= Cliente
        fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]
        widgets = {'cpf_cnpj': forms.TextInput(attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}),
                   'telefone': forms.TextInput(attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}),
                   'cep': forms.TextInput(attrs={'required': 'true', 'data-mask':"00000-000"})} """

""" class ClientePessoaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="Nome Completo")
    # cpf = BRCPFField(widget= BRCPFInput(
    #         attrs={'class': 'form-control','data-mask': '000.000.000-00', 'required': 'true'}), label="CPF")
    data_nascimento = forms.DateField(widget=forms.TextInput(
            attrs={'data-mask': '00/00/0000', 'required': 'true'}), label="Data de Nascimento")
    genero = forms.Select(
        attrs={'required': 'false'})
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000.000.000-00"}), label="CPF", max_length=11)
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    logradouro = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    numero = forms.IntegerField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    estado = forms.Select(
        attrs={'required': 'true'})
    cidade = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={'required': 'true'}))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000"}))

    class Meta:
        model= Cliente
        fields= ["nome", "senha", "cpf_cnpj", "data_nascimento", "genero", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]
        widgets = {'cpf_cnpj': forms.TextInput(attrs={'required': 'true', 'data-mask':"000-000-0000"}),
                   'telefone': forms.TextInput(attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}),
                   'cep': forms.TextInput(attrs={'required': 'true', 'data-mask':"00000-000"})} """

""" class ClientePessoaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="Nome Completo")
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"000.000.000-00"}), label="CPF", max_length=11)
    data_nascimento = forms.DateField(widget=forms.TextInput(
        attrs={'data-mask': '00/00/0000', 'required': 'true'}), label="Data de Nascimento")
    genero = forms.Select(
        attrs={'required': 'false'})
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'required': 'true'}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'id_pessoa_cep'}))
    logradouro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_pessoa_logradouro'}))
    numero = forms.IntegerField(widget=forms.TextInput(
        attrs={'required': 'true', 'maxlength':"5", 'id': 'id_pessoa_numero'}))
    bairro = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_pessoa_bairro'}))
    ESCOLHAS = (('', '----------'),) + ESTADO_CHOICES
    estado = forms.CharField(widget=forms.Select(choices=ESCOLHAS,
        attrs={'required': 'true', 'id': 'id_pessoa_estado'}))
    cidade = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'id': 'id_pessoa_cidade'}))
    
    class Meta:
        model= ClienteModel
        fields= ["nome", "senha", "cpf_cnpj", "data_nascimento", "genero", "email", "telefone", "cep", "logradouro", "numero", "bairro", "cidade", "estado"]
        # widgets = {'cpf_cnpj': forms.TextInput(attrs={'required': 'true', 'data-mask':"000-000-0000"}),
        #            'telefone': forms.TextInput(attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}),
        #            'cep': forms.TextInput(attrs={'required': 'true', 'data-mask':"00000-000", 'id': 'cep_teste_id'})}

class ClienteEmpresaForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="Nome Social")
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}), label="CNPJ")
    logradouro = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    telefone = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}))
    estado = forms.Select(
        attrs={'required': 'true'})
    cidade = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={'required': 'true'}))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))
    cep = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true', 'data-mask':"00000-000"}))

    class Meta:
        model= ClienteModel
        fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "logradouro", "numero", "bairro", "cidade", "estado", "cep"]
        widgets = {'cpf_cnpj': forms.TextInput(attrs={'required': 'true', 'data-mask':"00.000.000/0000-00"}),
                   'telefone': forms.TextInput(attrs={'required': 'true', 'data-mask':"(00) 00000-0000"}),
                   'cep': forms.TextInput(attrs={'required': 'true', 'data-mask':"00000-000"})} """

""" class RegistrarAdministradorForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="Nome Social")
    cpf_cnpj = forms.CharField(widget=forms.TextInput(
        attrs={'required': 'true'}), label="CNPJ", max_length=14)
    logradouro = forms.CharField(widget=forms.TextInput(
            attrs={'required': 'true'}))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={'required': 'true'}))
    senha = forms.CharField(widget=forms.PasswordInput(
        attrs={'required': 'true', 'minlength': '6'}))

    class Meta:
        model= FuncionariosModel
        fields= ["nome", "senha", "cpf_cnpj", "email", "telefone", "logradouro"] """

# models.py

""" class Reserva(models.Model):
    # id_reserva = models.AutoField(primary_key=True)
    # id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente')
    # id_pagamento = models.ForeignKey('Pagamento', models.DO_NOTHING, db_column='id_pagamento', blank=True, null=True)
    # datahora_log = models.DateTimeField()
    # id_espaco = models.ForeignKey('Espacos', models.DO_NOTHING, db_column='id_espaco')
    # id_pacote_horas = models.ForeignKey('Pacotehoras', models.DO_NOTHING, db_column='id_pacote_horas', blank=True, null=True)
    # data_reserva = models.DateField()
    # hora_entrada = models.TimeField(default=None, blank=True, null=True)
    # hora_entrada_real = models.TimeField(default=None, blank=True, null=True)
    # hora_saida = models.TimeField(default=None, blank=True, null=True)
    # hora_saida_real = models.TimeField()
    # hora_limpeza = models.TimeField()
    # hora_limpeza_real = models.TimeField()
    # preco_total = models.FloatField()

    # objects = GerenciaReserva()

    # class Meta:
    #     managed = False
    #     db_table = 'reserva'
    id_reserva = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_pagamento = models.ForeignKey(Pagamento, models.DO_NOTHING, db_column='id_pagamento', blank=True, null=True)
    id_espaco = models.ForeignKey(Espacos, models.DO_NOTHING, db_column='id_espaco')
    id_pacote_horas = models.ForeignKey(Pacotehoras, models.DO_NOTHING, db_column='id_pacote_horas', blank=True, null=True)
    data_reserva = models.DateField()
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    hora_limpeza = models.TimeField()
    datahora_log = models.DateTimeField(blank=True, null=True)
    hora_entrada_real = models.TimeField(blank=True, null=True)
    hora_saida_real = models.TimeField(blank=True, null=True)
    hora_limpeza_real = models.TimeField(blank=True, null=True)
    preco_total = models.FloatField(blank=True, null=True)
    objects = GerenciaReserva()

    class Meta:
        managed = False
        db_table = 'reserva' """

""" class Espacos(models.Model):
    STATUS_CHOICES = (
        ("0", "Ativo"),
        ("1", "Desativado")
    )

    # id_espaco = models.AutoField(primary_key=True)
    # # id_tipo_espaco = models.ForeignKey('Tipoespaco', models.DO_NOTHING, db_column='id_tipo_espaco')
    # id_tipo_espaco = models.ForeignKey(Tipoespaco, on_delete=models.CASCADE, related_name='espaco_id_tipo_espaco')
    
    # # preco = models.FloatField() // Retirado
    # # ultima_alteracao = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='id_funcionario')
    # ultima_alteracao = models.ForeignKey(Funcionarios, on_delete=models.CASCADE, db_column='espaco_id_funcionario')
    # status_espaco = models.IntegerField()
    # data_ultima_alteracao = models.DateTimeField()

    id_espaco = models.AutoField(primary_key=True)
    id_tipo_espaco = models.ForeignKey('Tipoespaco', models.DO_NOTHING, db_column='id_tipo_espaco')
    ultima_alteracao = models.ForeignKey('Funcionarios', models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    status_espaco = models.IntegerField(blank=True, null=True)
    data_ultima_alteracao = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(f'{self.id_tipo_espaco.nome}')#GABRIEL

    class Meta:
        managed = False
        db_table = 'espacos' """

""" class Tipoespaco(models.Model):

    # id_tipoespaco = models.AutoField(db_column='id_tipoEspaco', primary_key=True)  # Field name made lowercase.
    # descricao = models.CharField(max_length=200, blank=True, null=True)
    # nome = models.CharField(max_length=45)
    # ultima_alteracao = models.ForeignKey(Funcionarios, models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    # tempo_limpeza = models.TimeField(blank=True, null=True)
    # preco = models.FloatField(blank=True, null=True)
    # data_ultima_alteracao = models.DateTimeField(blank=True, null=True)

    id_tipoespaco = models.AutoField(db_column='id_tipoEspaco', primary_key=True)  # Field name made lowercase.
    descricao = models.CharField(max_length=200, blank=True, null=True)
    nome = models.CharField(max_length=45)
    ultima_alteracao = models.ForeignKey(Funcionarios, models.DO_NOTHING, db_column='ultima_alteracao', blank=True, null=True)
    tempo_limpeza = models.TimeField(blank=True, null=True)
    preco = models.FloatField(blank=True, null=True)
    data_ultima_alteracao = models.DateTimeField(blank=True, null=True)
    compartilhado = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'tipoEspaco' """

# views.py

""" def reserva2(request):
    date = datetime.datetime(2009,4,1)
    context = {'date': date}
    return render(request, 'reserva.html', {'date': date, 'num': 1}) """

""" from django.contrib.auth import authenticate, login
from gere_coworking.forms import *
def loginSystem(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if form.is_valid():
            login(request, user)
            grupo = 'grupo'

            l = request.user.groups.values_list('name',flat = True) # QuerySet Object
            l_as_list = list(l)
            grupo = str(l_as_list)

            return render(request, 'cliente_final/apresentacao/index.html', {'grupo': grupo})

    else:
        form = AuthenticationForm()
    return render(request, 'cliente_final/cadastro_e_login/loginSystem.html', {'form': form}) """

"""
# # Formatação das máscaras
# cliente.fields['cpf_cnpj'].label = str(cpf_cnpj).replace('.', '').replace('-', '')
"""

""" def registrarAdministrador(request):
    if request.method == "POST":
        funcionario = RegistrarAdministradorForm(request.POST)
        if funcionario.is_valid():
            cpf_cnpj = request.POST['cpf_cnpj']
            email = request.POST['email']
            senha = request.POST['senha']

            my_group = Group.objects.get(name='administrador')
            first_name = request.POST['nome'].capitalize().strip()
            last_name = ''
            
            
            # Salva na tabela user
            user = User.objects.create_user(username=cpf_cnpj, password=senha,
             email=email, first_name=first_name, last_name=last_name, is_superuser=True,
             is_staff=True)
            user.save()

            # Salva na tabela funcionario
            funcionario.save()

            # Configura um grupo de acesso para o usuário            
            my_group.user_set.add(user)

            return redirect('loginSystem')
        else:
            messages.error(request, 'Formulário inválido!')
            return redirect('registrarUsuario')
    else:
        form = RegistrarAdministradorForm
        return render(request, 'gerenciamentoCoworking/regAdministrator.html', {'form': form}) """

""" def agendamento(request, id_tipo_espaco):
    # Chama as reservas já feitas com uma data futura a hoje de um determinado tipo de espaço

    # Define se é uma sala privada (0) ou uma mesa compartilhada (1) por exemplo
    compartilhado = list(Tipoespaco.objects.filter(
            id_tipoespaco = id_tipo_espaco
        ))[0].compartilhado
    
    '''IMPRIME NA TELA AS RESERVAS DO PRÓPRIO CLIENTE'''
    event_list = []
    reservas = Reserva.objects.get_reservas_cliente(cpf_cnpj = request.user.username, id_tipo_espaco = id_tipo_espaco)
    for reserva in reservas:
        inicioReserva = datetime.datetime.combine(reserva.data_reserva, reserva.hora_entrada)
        fimReserva = datetime.datetime.combine(reserva.data_reserva, reserva.hora_saida)
        event_list.append({
                    'title': 'Sua reserva',
                    'start': inicioReserva.strftime("%Y-%m-%dT%H:%M:%S"),
                    'end': fimReserva.strftime("%Y-%m-%dT%H:%M:%S"),
                    'color': 'lightblue',
                    'textColor': 'black',
                    # 'display': 'list-item'
                })

    '''IMPRIME NA TELA AS VAGAS JÁ RESERVADAS'''
    reservas = Reserva.objects.get_reservas_atuais(id_tipo_espaco = id_tipo_espaco)
    # HORÁRIO COMERCIAL DO COWORKING
    businessHours = [{
        # days of week. an array of zero-based day of week integers (0=Sunday)
        'daysOfWeek': [ 1, 2, 3, 4, 5 ], # Monday - Friday

        'startTime': '07:00', # a start time (07:00, 07:30, 08:00) (10am in this example)
        'endTime': '22:00', # an end time (6pm in this example)
        },
        {
            'daysOfWeek': [ 6, 0 ], # Saturday, Sunday
            'startTime': '09:00', # a start time (10am in this example)
            'endTime': '19:00', # an end time (6pm in this example)
        }]

    # Dicionário de datas para rastrear reservas concorrentes
    dateDicts = {}
    # dateDicts = [{'2021-07-28T00:00:00': {
    #     '07:00': 0,
    #     '07:30': 1,
    #     '08:00': 1,
    #     '08:30': 1,
    #     '09:00': 0
    # }}, {'2021-07-31T00:00:00': {
    #     '07:00': 0,
    #     '07:30': 1,
    #     '08:00': 1,
    #     '08:30': 1,
    #     '09:00': 0
    # }}]
    datasRastreadas = []

    # Popula o dicionário
    for reserva in reservas:
        data = reserva.data_reserva
        entrada = datetime.datetime.combine(reserva.data_reserva, reserva.hora_entrada)
        saida = datetime.datetime.combine(reserva.data_reserva, reserva.hora_saida)

        # Cria um novo dicionário de horas para uma data caso ela não exista
        if data not in datasRastreadas:
            datasRastreadas.append(data)
            diaSemana = data.weekday() # [0 - monday, 1 - tuesday, 6 - sunday]
            if diaSemana == 6:
                diaSemana = 0
            else:
                diaSemana += 1
            # diaSemana [0 - sunday, 1 - monday, 6 - saturday]
            
            for dicionario in businessHours:
                if diaSemana in dicionario['daysOfWeek']:
                    jsonObj = {}
                    hora = datetime.datetime.strptime(dicionario['startTime'], "%H:%M")
                    horaFim = datetime.datetime.strptime(dicionario['endTime'], "%H:%M")
                    
                    # print('---------------- A', file=sys.stderr)
                    # print('hora = ', hora.strftime("%Y-%m-%d %H:%M"), file=sys.stderr)
                    # print('horaFim = ', horaFim.strftime("%Y-%m-%d %H:%M"), file=sys.stderr)

                    while hora <= horaFim:
                        jsonObj[hora.strftime("%H:%M")] = 0
                        hora += datetime.timedelta(minutes=30)
                        # print('hora Depois = ', hora.strftime("%Y-%m-%d %H:%M"), file=sys.stderr)
                    dateDicts[data.strftime("%Y-%m-%d")] = jsonObj
                    break
        
        # Marca as horas desta reserva no dicionário
        hora = entrada
        horaJson = entrada
        hour, minute = dicionario['startTime'].split(':')
        horaJson = entrada.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        while hora < saida:
            if entrada <= horaJson:
                hora += datetime.timedelta(minutes=30)
                # Incrementa o campo do JSON com um valor a mais
                dateDicts[data.strftime("%Y-%m-%d")][horaJson.strftime("%H:%M")] += 1
            horaJson += datetime.timedelta(minutes=30)    
    
    '''Importante'''
    vagas_max = 2

    # Lê os dias das reservas
    for data, horarios in dateDicts.items():
        comecoEvento = False # Lógica de verificação do começo do evento
        inicio = None # Para salvar o horário do começo do evento

        # Lê as horas de um dia das reservas
        for hora, valor in horarios.items():

            # Começa a rastrear o tamanho do evento
            if valor >= vagas_max and comecoEvento == False:
                comecoEvento = True
                inicio = hora

            # Conclui o fim do evento e define a lógica de setar o evento
            if comecoEvento == True and valor < vagas_max :
                comecoEvento = False
                fim = hora

                ##############################################################################################
                # Confere os eventos de reserva do cliente para dar prioridade pro evento do cliente na tela 
                ##############################################################################################
                reservasDoDia = []

                # Separa os eventos relativos ao dia que se quer analisar
                for evento in event_list:
                    dataEvento = datetime.datetime.strptime(evento['start'], "%Y-%m-%dT%H:%M:%S").replace(hour=0, minute=0, second=0, microsecond=0)
                    dataAtual = datetime.datetime.strptime(data, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
                    if dataEvento == dataAtual:
                        reservasDoDia.append(evento)

                # Evento lotado = evento que há indisponibilidade de vagas (cor vermelha)
                # Reserva neste contexto = reserva do cliente no dia (cor azul)
                for evento in reservasDoDia:
                    comecoReserva = datetime.datetime.strptime(evento['start'], "%Y-%m-%dT%H:%M:%S").replace(year=2020, month=1, day=1)
                    fimReserva = datetime.datetime.strptime(evento['end'], "%Y-%m-%dT%H:%M:%S").replace(year=2020, month=1, day=1)
                    comecoEventoLotado = datetime.datetime.strptime(inicio, "%H:%M").replace(year=2020, month=1, day=1)
                    fimEventoLotado = datetime.datetime.strptime(fim, "%H:%M").replace(year=2020, month=1, day=1)

                    if comecoReserva <= comecoEventoLotado and comecoEventoLotado <= fimReserva:
                        inicio = fimReserva.strftime("%H:%M")
                    if comecoReserva <= fimEventoLotado and comecoEventoLotado <= fimReserva:
                        fim = comecoReserva.strftime("%H:%M")
                ##############################################################################################

                ano, mes, dia = data.split('-')
                hour, minutes = inicio.split(':')
                start = f'{ano}-{mes}-{dia}T{hour}:{minutes}:00'
                hour, minutes = fim.split(':')
                end = f'{ano}-{mes}-{dia}T{hour}:{minutes}:00'
                # print('------------- VARS', file=sys.stderr)
                # print(start, file=sys.stderr)
                # print(end, file=sys.stderr)
                event_list.append({
                    'title': 'Sem vagas',
                    'start': start,
                    'end': end,
                    'color': 'red',
                    'textColor': 'black',
                    # 'display': 'list-item'
                })

    
    # print('------------- EVENT LIST', file=sys.stderr)
    # print(event_list, file=sys.stderr)



    # # As reservas são convertidas em eventos para serem lidas pelo programa
    # for reserva in reservas:
    #     # combinar() = datetime.datetime.combine()
    #     datetime_entrada = datetime.datetime.combine(reserva.data_reserva, reserva.hora_entrada)
    #     datetime_saida = datetime.datetime.combine(reserva.data_reserva, reserva.hora_saida)
    #     event_list.append({
    #         # 'title': event.title,
    #         'start': datetime_entrada.date().strftime("%Y-%m-%dT%H:%M:%S"),
    #         'end': datetime_saida.date().strftime("%Y-%m-%dT%H:%M:%S"),
    #     })
    
    hasErrors = False
    error = None
    if request.method == 'POST':
        hora_entrada = request.POST['hora-entrada'].split(' ')[0]
        hora_saida = request.POST['hora-saida'].split(' ')[0]
        if compartilhado:
            id_espaco = 1
        else:
            id_espaco = request.POST['id_espaco']

        # Lógica para pegar 'hora_limpeza'
        espaco = list(Espacos.objects.filter(
            id_espaco = id_espaco
        ))[0]
        hora, minuto, segundo = hora_saida.split(':')
        dataHoraSaida = datetime.datetime.today().replace(hour=int(hora), minute=int(minuto), second=int(segundo))
        hourDelta, minDelta, segDelta = espaco.id_tipo_espaco.tempo_limpeza.strftime("%H %M %S").split(' ')
        hora_limpeza = dataHoraSaida + datetime.timedelta(hours=int(hourDelta), minutes=int(minDelta), seconds=int(segDelta))

        cliente = list(Cliente.objects.filter(
            cpf_cnpj = request.user.username
        ))[0]
        
        # hoje = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        hoje = datetime.datetime.today()
        preco = espaco.id_tipo_espaco.preco
        dicionario = {
            'id_cliente': cliente.id_cliente,
            'id_espaco': id_espaco,
            'data_reserva': request.POST['data-reserva'],
            'hora_entrada': hora_entrada,
            'hora_saida': hora_saida,
            'hora_limpeza': hora_limpeza.strftime("%H:%M:%S"),
            'datahora_log': hoje,
            'hora_entrada_real': '',
            'hora_saida_real': '',
            'hora_limpeza_real': '',
            'preco_total': preco,
            }
        
        form = FormReservaForm(dicionario)
        if form.is_valid():
            hora_entrada = datetime.datetime.strptime(dicionario['hora_entrada'], "%H:%M:%S")
            hora_saida = datetime.datetime.strptime(dicionario['hora_saida'], "%H:%M:%S")
            dataReserva = datetime.datetime.strptime(dicionario['data_reserva'], "%d/%m/%Y")
            hoje = datetime.datetime.today()

            if hora_entrada > hora_saida:
                hasErrors = True
                error = 'ERRO! A hora de entra não pode ser menor que a hora de saída.'
            elif dataReserva < hoje:
                hasErrors = True
                error = 'ERRO! A data informada já passou!'
            elif (hora_saida - hora_entrada) < datetime.timedelta(minutes=30):
                hasErrors = True
                error = 'ERRO! O tempo mínimo de reserva é 30 minutos.'
            elif (dataReserva - hoje) > datetime.timedelta(days=30):
                hasErrors = True
                error = 'ERRO! Não é possível realizar reservas de forma programática para mais de 30 dias. Entre em contato conosco.'
            else:
                # Confere os eventos reservados
                for evento in event_list:
                    hora, minuto, segundo = dicionario['hora_entrada'].split(':')
                    dhora_entrada = datetime.datetime.combine(dataReserva, datetime.time(int(hora), int(minuto), int(segundo)))
                    hora, minuto, segundo = dicionario['hora_saida'].split(':')
                    dhora_saida = datetime.datetime.combine(dataReserva, datetime.time(int(hora), int(minuto), int(segundo)))
                    inicioEvento = datetime.datetime.strptime(evento['start'], '%Y-%m-%dT%H:%M:%S')
                    fimEvento = datetime.datetime.strptime(evento['end'], '%Y-%m-%dT%H:%M:%S')
                    if (inicioEvento < dhora_entrada and dhora_entrada < fimEvento) or (inicioEvento < dhora_saida and dhora_saida < fimEvento):
                        hasErrors = True
                        error = 'Horário já reservado. Escolha outro.'
                        break
                diaSemana = dataReserva.weekday()

                # Converte dia da semana para modelo do full calendar
                if diaSemana == 6:
                    diaSemana = 0
                else:
                    diaSemana += 1
                
                # Confere se a hora está dentro do horário comercial válido
                for dicionario in businessHours:
                    if diaSemana in dicionario['daysOfWeek']:
                        horarioAbertura = datetime.datetime.strptime(dicionario['startTime'], "%H:%M")
                        horarioFechamento = datetime.datetime.strptime(dicionario['endTime'], "%H:%M")
                        if (hora_entrada < horarioAbertura) or (hora_saida > horarioFechamento):
                            hasErrors = True
                            error = 'Fora de horário comercial, tente outro horário.'
                        break
            
            # Salva o formulário se ele não contiver erros
            if not hasErrors:
                form.save()
                context = {
                    'token': True,
                    'reservas': reservas,
                }
                return redirect('listarReservas')
        else:
            error = 'Formulário inválido: '
            for k, v in form.errors.as_json.items():
                error += f'Campo {k} : {v}'

    else:
        form = FormReservaForm

    context = {
        # 'reservas': reservas,
        'eventos': event_list,
        'form': form,
        'hasErrors': hasErrors,
        'error': error,
        'compartilhado': compartilhado,
    }
    return render(request, 'agendamento.html', context) """

""" def registrarUsuario(request):
    if request.method == "POST":
        data = b_cadastro.getDicionarioClienteForm(request)
        data['cpf_cnpj'] = h.retiraSimbolosString(data['cpf_cnpj'])


        cliente = ClientePessoaForm(data)
        
        if cliente.is_valid():
            user = b_cadastro.escreveNaTabelaUser(json=data, pessoa=True)
            cliente.save()  # Salva na tabela cliente
            b_cadastro.configuraGrupoUsuario(user, tipo='pessoa')
            return redirect('loginSystem')
        
        empresa = ClienteEmpresaForm(data)
        if empresa.is_valid():
            user = b_cadastro.escreveNaTabelaUser(json=data, pessoa=False)
            empresa.save()  # Salva na tabela cliente
            b_cadastro.configuraGrupoUsuario(user, tipo='empresa')
            return redirect('loginSystem')

        messages.error(request, request.POST)

    else:
        cliente = ClientePessoaForm
        empresa = ClienteEmpresaForm
    return render(request, 'cliente_final/cadastro_e_login/regUsers.html', {'pessoaForm': cliente, 'empresaForm':empresa}) """

# views_helper.py

""" def getFormMensagemErro(Form):
    erros = Form.errors.get_json_data(escape_html=False)
    if len(erros) == 0:
        return 'Sem erros'
    elif len(erros) == 1:
        mensagem = f'{erros["__all__"][0]["message"]}'
        return mensagem
    else:
        return 'Sem erros'
        return Form.errors.as_json(escape_html=False) """
