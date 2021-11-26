from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from domains.models import Domain
from cria_coworking.models import Administrador
from cria_coworking.forms import RegistrarAdministradorForm
import common.views_manager as m
import custom_templates.services as s
import custom_templates.selectors as sc
from custom_templates.models import InstanceConfig
from custom_templates.forms import FormInstanceConfig
import os, json

# Create your views here.
@m.verificador()
def render_view(request, context):
    # context['batata'] = 'batata é muito bom'

    
    
    # content = render_to_string('gere/template1/cliente/apresentacao/index_custom.html', context)
    # # print(content)

    # exists = os.path.exists('templates/gere/template1')
    # template = s.create_path_if_does_not_exist('templates/instances/cliente/apresentacao/index.html')
    # with open(template, 'w', encoding="utf-8") as static_file:
    #     static_file.write(content)
    
    # context['batata'] = 'batatona'
    
    s.mount_client_base(request, context)
    s.mount_client_index(request, context)
    

    return render(request, 'instances/cliente/apresentacao/index.html', context)

@m.verificador()
def teste_render(request, context):
    context['batata'] = "'%s'"%request.LANGUAGE_CODE
    adm = Administrador.objects.using('default').get(id=12)
    s.delete_client_configs(adm.id)
    s.instantiate_config(cliente=adm)
    s.instantiate_template_index(cliente=adm)
    # Administrador.objects.using('default').get(id=12).nome
    return render(request, 'gere/template1/cliente/apresentacao/index.html', context)

@m.verificador()
def custom_index(request, context):
    if request.method == 'POST':
        valid = s.process_post_custom_view(request, context)
        if valid:
            ...
            # return redirect('menuAdmin')
    context = s.get_context_custom_index(request, context)
    
    return render(request, 'gere/template1/adm/customizar_templates/custom_index.html', context)

@m.verificador()
def custom_cowork_info(request, context):
    instance = InstanceConfig.objects.get(client_id=sc.get_current_adm_by_request(request))
    if request.method == 'POST':
        dados = dict(request.POST)
        print('-- dados?? --')
        print(dados)
        for key, value in dados.items():
            dados[key] = value[0]
        if 'client_logo' not in dados:
            dados['client_logo'] = request.FILES['client_logo']
        print(dados)
        dados['color_palette'] = {'1st': request.POST['paleta1'],
                                  '2nd': request.POST['paleta2'],
                                  '3rd': request.POST['paleta3'],
                                  'button': request.POST['button_design']}
        form = FormInstanceConfig(data=dados, instance=instance)
        if form.is_valid():
            form_aux = form.save(commit=False)
            if dados['client_logo'] != '':
                form_aux.client_logo = dados['client_logo']
            form_aux.save()
            s.mount_all_customs(request, context)
            return redirect('custom_cowork_info')
    else:
        if isinstance(instance.color_palette, dict):
            paleta = instance.color_palette
        else:
            paleta = json.loads(instance.color_palette.replace("'", "\""))
        form = FormInstanceConfig(instance=instance,
                                  initial={'paleta1': paleta.get('1st'),
                                           'paleta2': paleta.get('2nd'),
                                           'paleta3': paleta.get('3rd'),})
        context['button'] = paleta['button']

    context['form'] = form
    return render(request, 'gere/template1/adm/customizar_templates/custom_cowork_info.html', context)

@m.verificador()
def custom_personal_info(request, context):
    if request.method == 'POST':
        form = RegistrarAdministradorForm(data=request.POST, 
                                          exclude_fields=['senha', 'domain'],
                                          instance=sc.get_current_adm_by_request(request))
        if form.is_valid():
            form.save()
            s.mount_all_customs(request, context)
            ...
    else:
        form = RegistrarAdministradorForm(exclude_fields=['senha', 'domain'], 
                                          instance=sc.get_current_adm_by_request(request))

    context['form'] = form
    return render(request, 'gere/template1/adm/customizar_templates/custom_personal_info.html', context)