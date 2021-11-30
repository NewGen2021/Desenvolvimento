from django.shortcuts import render
from django.conf import settings
from django.utils.translation import gettext as _
from functools import wraps
from common.selectors import get_administrador_by_request, get_button_by_administrador
import sys

MAIN_HOST = settings.MAIN_HOST

class ForgottenArgs(Exception):
    pass

def verificador(cria_coworking=False, need_adm=False):
    def inner(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            # cria_coworking = False if not hasattr(kwargs, 'cria_coworking') else kwargs['cria_coworking']
            # need_adm = False if not hasattr(kwargs, 'need_adm') else kwargs['need_adm']
            response = verify_view(request, cria_coworking, need_adm)
            if response.get('render') is not None:
                return response['render']
            context = response['context']
            return view(request, context, *args, **kwargs)
        return wrapper
    return inner

def get_url_without_langcode(request):
    cur_url = request.get_full_path()
    list_without_lang = cur_url.split('/')[2:]
    return '/'.join(list_without_lang)

def verify_view(request, criaCoworking: bool, needAdm: bool):
    response = {}
    adm = get_administrador_by_request(request)
    response['context'] = {
        'turl': get_url_without_langcode(request),
        'domain': str(request.domain['domain']),
    }
    if request.domain['domain'] != MAIN_HOST:    
        response['context']['button_color'] = get_button_by_administrador(adm)
        response['context']['base_template'] = f'instances/{adm.id}/base.html'

    if request.domain['domain'] is None:
        print('ERRO 1', file=sys.stderr)
        response['context']['error_message'] = _('O seguinte sistema não existe.')
        response['render']  = render(request, 'erros/erroGenerico.html', response['context'])
        return response
    if request.domain['isActive'] is False:
        print('ERRO 2', file=sys.stderr)
        response['context']['error_message'] = _('O seguinte sistema atualmente está desativado.')
        response['render']  = render(request, 'erros/erroGenerico.html', response['context'])
        return response
    # if request.domain['domain'].domain == MAIN_HOST:  # with database
    if request.domain['domain'] == MAIN_HOST:  # with json
        # if criaCoworking is False:
        #     print('ERRO 3', file=sys.stderr)
        #     response['context']['error_message'] = _(f'A seguinte página se refere a um sistema cliente, não ao sistema newgen.')
        #     response['render']  = render(request, 'erros/erroGenerico.html', response['context'])
        #     return response
        pass
    return response

def get_template():
    pass