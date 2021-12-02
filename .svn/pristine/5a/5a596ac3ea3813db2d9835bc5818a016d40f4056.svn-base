import json
import os

from django.template.loader import render_to_string
from dns.flags import AD
from .models import *
import custom_templates.selectors as selectors
import common.services as c
import common.selectors as cselc


def escape_tags(html_string: str) -> str:
    html_string = html_string.replace('{%', '{%templatetag openblock%}')
    html_string = html_string.replace(' %}', '{%templatetag closeblock%}')
    html_string = html_string.replace('{{', '{%templatetag openvariable%}')
    html_string = html_string.replace(' }}', '{%templatetag closevariable%}')
    return html_string


def get_html_string(path: str, escape_django_tags: bool=False) -> str:
    with open(path, "rb") as fp:                      
        unicode_html = fp.read().decode('utf-8', 'ignore')
        fp.close()
        return escape_tags(unicode_html) if escape_django_tags else unicode_html


def split_path(path: str) -> list:
    def split_paths(path: str) -> list:
        paths = [os.path.split(path)[1]]
        if path != "":
            paths += split_paths(os.path.split(path)[0])
        return paths

    paths = split_paths(path)[:-1]
    return paths[::-1]


def create_path_if_does_not_exist(path: str) -> str:
    paths = split_path(path)
    current = ''
    for path in paths:
        current = os.path.join(current, path)
        if not os.path.exists(current) and path.find('.') == -1:
            os.mkdir(current)
    return current


def instantiate_config(cliente: Administrador):
    file = open('static/img/default-logo.png', 'rb')
    InstanceConfig.objects.using('default').create(
        client_id=cliente,
        color_palette="{'1st':'5382ab','2nd':'428bca','3rd':'7cadd7','button':'btn-primary'}",
        client_logo='template_index/default/default-logo.png',
        showing_company_name=cliente.nome,
    )


def instantiate_custom_config(cliente: Administrador, nome: str, 
                              cor1: str, cor2: str, cor3: str, button: str, client_logo):
    file = open('static/img/default-logo.png', 'rb')
    Instance, success = InstanceConfig.objects.using('default').get_or_create(
        client_id=cliente
    )
    Instance.color_palette="{'1st':'%s','2nd':'%s','3rd':'%s','button':'%s'}" %(cor1, cor2, cor3, button)
    Instance.client_logo=client_logo
    Instance.showing_company_name=nome
    Instance.save()
    return success

def instantiate_template_index(cliente: Administrador):
    index = TemplateIndex.objects.using('default').create(
        client_id=cliente,
        has_carousel_slides=1,
        has_services=1,
        has_contact=1,
        about_us={'pt-br': {'title': 'Sobre Nós',
                            'description': 'Somos mais que um simples coworking, nascemos com um propósito muito '
                                           'maior, o de apoiar pequenos e médios empresários, profissionais autônomos, '
                                           'empreendedores, startup e todos aqueles sonhadores que merecem um espaço '
                                           'com toda infra estrutura necessária para seu projeto decolar.'},
                  'en': {'title': 'About us',
                         'description': 'We are more than a simple coworking, we were born with a much greater '
                                        'purpose, that of supporting small and medium entrepreneurs, self-employed '
                                        'professionals, entrepreneurs, startups and all those dreamers who deserve a '
                                        'space with all the necessary infrastructure for their project to take off.'}},
    )
    button = ResourceButtons.objects.using('default').create(
        client_id=cliente,
        button_tipo=1,
        text={'pt-br': {'title': 'Faça seu agendamento', 'href': 'reserva'},
              'en': {'title': 'Make your appointment', 'href': 'reserva'}, }
    )
    ResourceCarouselSlide.objects.using('default').create(
        client_id=cliente,
        id_index=index,
        id_button=None,
        text={'pt-br': {'title': 'Networking e Economia',
                        'description': 'Reduzindo custos para sua empresa e proporcionando colaboração mútua.'},
              'en': {'title': 'Networking and Saving',
                     'description': 'Reducing costs for your company and providing mutual collaboration.'}},
        image='template_index/default/slide-1.jpg'
    )
    ResourceCarouselSlide.objects.using('default').create(
        client_id=cliente,
        id_index=index,
        id_button=button,
        text={'pt-br': {'title': 'Agendamento On-line',
                        'description': 'Encontre o melhor espaço para você trabalhar.'},
              'en': {'title': 'Online Scheduling',
                     'description': 'Find the best space to work.'}},
        image='template_index/default/slide-2.jpg'
    )
    ResourceCarouselSlide.objects.using('default').create(
        client_id=cliente,
        id_index=index,
        id_button=None,
        text={'pt-br': {'title': 'Infraestrutura',
                        'description': 'O Coworking elaborado é o lugar perfeito para você reder ao máximo.'},
              'en': {'title': 'Infrastructure',
                     'description': 'The elaborate Coworking is the perfect place for you to network to the fullest.'}},
        image='template_index/default/slide-3.jpg'
    )
    ResourceServices.objects.using('default').create(
        client_id=cliente,
        bootstrap_icon='easel',
        text={'pt-br': {'title': 'Auditório',
                        'description': 'O espaço perfeito para as suas palestras ou treinamentos serem um sucesso!'},
              'en': {'title': 'Auditorium',
                     'description': 'The perfect space for your lectures or training to be a success!'}},
    )
    ResourceServices.objects.using('default').create(
        client_id=cliente,
        bootstrap_icon='people-fill',
        text={'pt-br': {'title': 'Estações de Trabalho',
                        'description': 'Reduza os custos com sabedoria! Conheça as nossas estações de trabalho e faça '
                                       'parte do time.'},
              'en': {'title': 'Work stations',
                     'description': 'Reduce costs wisely! Discover our workstations and join the team.'}},
    )
    ResourceServices.objects.using('default').create(
        client_id=cliente,
        bootstrap_icon='door-open',
        text={'pt-br': {'title': 'Salas Executivas',
                        'description': 'Amplo espaço para os seus eventos ou reuniões com uma grande demanda.'},
              'en': {'title': 'Executive Rooms',
                     'description': 'Ample space for your events or meetings in great demand.'}},
    )
    ResourceServices.objects.using('default').create(
        client_id=cliente,
        bootstrap_icon='shield-check',
        text={'pt-br': {'title': 'Salas de reuniões exclusivas',
                        'description': 'Desejando um pouco mais de privacidade para as suas reuniões? Nós temos a '
                                       'solução!'},
              'en': {'title': 'Exclusive meeting rooms',
                     'description': 'Wishing a little more privacy for your meetings? We have the solution!'}},
    )
    ResourceServices.objects.using('default').create(
        client_id=cliente,
        bootstrap_icon='person-circle',
        text={'pt-br': {'title': 'Secretária compartilhada',
                        'description': 'Deixe a comodidade conosco! Contamos com uma equipe capacitada para a recepção.'},
              'en': {'title': 'Shared Secretary',
                     'description': 'Leave the convenience to us! We have a qualified reception team.'}},
    )
    ResourceServices.objects.using('default').create(
        client_id=cliente,
        bootstrap_icon='geo-alt',
        text={'pt-br': {'title': 'Endereço fiscal e comercial',
                        'description': 'Seja para quem está começando ou não, nós te damos o auxílio que você precisa!'},
              'en': {'title': 'Tax and business address',
                     'description': 'Whether you are starting or not, we give you the help you need!'}},
    )
    text = {'pt-br': {'title': '', 'description': ''},
            'en': {'title': '', 'description': ''}},


def delete_client_configs(cliente_id: int):
    models = [ResourceCarouselSlide, ResourceServices, InstanceConfig, ResourceButtons, TemplateIndex]

    for model in models:
        model.objects.using('default').filter(client_id=cliente_id).delete()


def mount_client_index(cliente: Administrador, context: dict) -> None:
    context = get_context_custom_index(cliente, context)
    # cliente = selectors.get_current_adm_by_request(request)
    content = render_to_string('gere/template1/cliente/apresentacao/index_custom.html', context)
    template = create_path_if_does_not_exist(f'templates/instances/{cliente.id}/cliente/apresentacao/index.html')
    with open(template, 'w', encoding="utf-8") as static_file:
        static_file.write(content)


def mount_client_base(cliente: Administrador, context: dict) -> None:
    context = get_context_custom_base(cliente, context)
    content = render_to_string('gere/template1/base_custom.html', context)
    template = create_path_if_does_not_exist(f'templates/instances/{cliente.id}/base.html')
    with open(template, 'w', encoding="utf-8") as static_file:
        static_file.write(content)


def mount_all_customs(cliente: Administrador, context: dict) -> None:
    mount_client_index(cliente, context)
    mount_client_base(cliente, context)


def get_context_custom_base(cliente: Administrador, context: dict) -> Administrador:
    # cliente = selectors.get_current_adm_by_request(request)
    instancia = InstanceConfig.objects.get(client_id=cliente)
    paleta = instancia.color_palette
    context['nome_empresa'] = instancia.showing_company_name
    context['logradouro'] = cliente.logradouro
    context['cep'] = f'{cliente.bairro} {cliente.cep},'
    context['cidade'] = f'{cliente.cidade} - {cliente.estado}'
    context['email'] = cliente.email
    context['menu_administrador'] = get_html_string('templates/gere/template1/base_include_admin.html', True)
    context['menu_funcionario'] = get_html_string('templates/gere/template1/base_include_func.html', True)
    if isinstance(paleta, str):
        paleta = json.loads(paleta.replace("'", "\""))
    context['cor1'] = paleta.get('1st')
    context['cor2'] = paleta.get('2nd')
    context['cor3'] = paleta.get('3rd')
    return context


def get_endereco(cliente: Administrador) -> str:
    return f'{cliente.logradouro}, {cliente.numero}, {cliente.bairro}, {cliente.cidade} - {cliente.estado}, {cliente.cep} '


def get_context_custom_index(cliente: Administrador, context: dict) -> dict:
    # cliente = selectors.get_current_adm_by_request(request)
    print('CLIENTE VOCÊ É OQ ?????????????????????????')
    print(cliente)
    context['slides'] = ResourceCarouselSlide.objects.using('default').filter(client_id=cliente)
    context['instance'] = InstanceConfig.objects.using('default').filter(client_id=cliente)[0]
    context['template_customs'] = TemplateIndex.objects.using('default').filter(client_id=cliente)[0]
    context['template_customs'].about_us = c.json_to_safe_html_string(context['template_customs'].about_us)
    context['services'] = ResourceServices.objects.using('default').filter(client_id=cliente)
    context['endereco'] = get_endereco(cliente)
    context['email'] = cliente.email
    context['botoes'] = ResourceButtons.objects.using('default').filter(client_id=cliente)
    for index, slide in enumerate(context['slides']):
        slide.text = str(json.dumps(slide.text)).replace("{", '&#x7B;').replace('}', '&#x7D;')
        slide.active = 'active' if index == 0 else ''

    i = 0
    for index, service in enumerate(context['services']):
        service.text = str(json.dumps(service.text)).replace("{", '&#x7B;').replace('}', '&#x7D;')
        service.fade = None if i == 0 else i
        i += 100
    return context


def process_post_custom_view(request, context):
    id_adm = cselc.get_administrador_id_by_domain(context['domain'])

    def get_index_images(index_inputs) -> dict:
        key = 'logo_image'
        if request.POST.get(key) is None:
            index_inputs[key] = request.FILES[key]
        return index_inputs

    def get_slides_images(slides_inputs: dict) -> dict:
        ids = []
        # get slides inputs ids
        for key, value in slides_inputs.items():
            if key in ['language', 'id_adm']:
                continue
            # "slide/31/slide_button_text"
            # "slide/32/slide_image"
            identifier = key.split('/')
            slide_id = identifier[1]
            if slide_id not in ids:
                ids.append(slide_id)
        # Get image from request.FILES if request.POST doesnt contain an image
        for slide_id in ids:
            key = f"slide/{slide_id}/slide_image"
            if request.POST.get(key) is None:
                slides_inputs[key] = request.FILES[key]

        return slides_inputs

    services_inputs = {'language': request.LANGUAGE_CODE, 'id_adm': id_adm}
    slides_inputs = {'language': request.LANGUAGE_CODE, 'id_adm': id_adm}
    index_inputs = {'language': request.LANGUAGE_CODE, 'id_adm': id_adm}
    for key, value in request.POST.items():
        if key == 'csrfmiddlewaretoken':
            continue
        # EXEMPLOS DE INPUTS:
        # "slide/31/slide_title"
        # "service/2/service_icon"
        # "about_us_description"
        identifiers = key.split('/')
        if identifiers[0] == 'slide':
            slides_inputs[key] = value
            continue
        if identifiers[0] == 'service':
            services_inputs[key] = value
            continue
        if 'contato' not in key:
            index_inputs[key] = value
    index_inputs = get_index_images(index_inputs)
    slides_inputs = get_slides_images(slides_inputs)

    return update_index_fields(index_inputs) and update_services_fields(services_inputs) and update_slides_fields(
        slides_inputs)


def update_index_fields(index_inputs: dict) -> bool:
    language = c.get_default_language_if_language_code_doesnt_exist(index_inputs['language'])
    id_adm = index_inputs.get('id_adm')
    instance_configs = InstanceConfig.objects.using('default').get(client_id=id_adm)
    template_index = TemplateIndex.objects.using('default').get(client_id=id_adm)
    administrador = Administrador.objects.using('default').get(id=id_adm)

    ''' logo_image update '''
    if index_inputs['logo_image'] != '':
        instance_configs.client_logo = index_inputs['logo_image']
    ''' about_us_description update '''
    json = template_index.about_us
    json[language]['description'] = index_inputs['about_us_description']
    template_index.about_us = json
    ''' select_email update '''
    administrador.email = index_inputs['select_email']

    ''' saving updates '''
    instance_configs.save(using='default')
    template_index.save(using='default')
    administrador.save(using='default')
    return True


def update_services_fields(services_inputs: dict) -> bool:
    language = c.get_default_language_if_language_code_doesnt_exist(services_inputs['language'])
    id_adm = services_inputs.get('id_adm')
    services = ResourceServices.objects.using('default').filter(client_id=id_adm)
    for service in services:
        service_id = service.id
        ''' title update '''
        json = service.text
        json[language]['title'] = services_inputs[f'service/{service_id}/service_title']
        service.text = json
        ''' description update '''
        json[language]['description'] = services_inputs[f'service/{service_id}/service_description']
        service.text = json
        ''' icon update '''
        service.bootstrap_icon = services_inputs[f'service/{service_id}/service_icon']
        service.save(using='default')
    return True


def update_slides_fields(slides_inputs: dict) -> bool:
    language = c.get_default_language_if_language_code_doesnt_exist(slides_inputs['language'])
    id_adm = slides_inputs.get('id_adm')
    slides = ResourceCarouselSlide.objects.using('default').filter(client_id=id_adm)
    for slide in slides:

        slide_id = slide.id
        ''' title update '''
        json = slide.text
        json[language]['title'] = slides_inputs[f'slide/{slide_id}/slide_title']
        slide.text = json
        ''' description update '''
        json[language]['description'] = slides_inputs[f'slide/{slide_id}/slide_description']
        slide.text = json
        ''' button update '''
        if tipo := int(slides_inputs[f'slide/{slide_id}/slide_button_tipo']):
            button = ResourceButtons.objects.get(client_id=id_adm, button_tipo=tipo)
            slide.id_button = button
            json = button.text
            texto = slides_inputs[f'slide/{slide_id}/slide_button_text']
            if texto:
                json[language]['title'] = texto
            button.text = json
            button.save(using='default')
        else:
            slide.id_button = None
        ''' logo_image update '''
        if slides_inputs[f'slide/{slide_id}/slide_image'] != '':
            slide.image = slides_inputs[f'slide/{slide_id}/slide_image']
        slide.save(using='default')
    return True
