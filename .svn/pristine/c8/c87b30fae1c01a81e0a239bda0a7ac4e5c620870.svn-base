from django import template
import json
import html
register = template.Library()

def custom_template_translate_json(data, arg):
    """{% load client_translation %}"""
    """{{ text_json | translate_json:request.LANGUAGE_CODE | translate_json:'title'}}"""
    """{{ text_json | translate_json:request.LANGUAGE_CODE | translate_json:'description'}}"""
    
    if data == None or data == '':
        return ''
    
    # Se não for title ou description, é um código de língua tipo "pt-br"
    if arg not in ['title', 'description']:
        string = html.unescape(data) 
        d: dict = json.loads(html.unescape(string))
        return str(json.dumps(d[arg]))
    d: dict = json.loads(data)
    return d[arg]

register.filter('custom_template_translate_json', custom_template_translate_json)

@register.simple_tag
def get_flag(lang_code):
    flag_code = ''
    if lang_code == 'pt-br':
        flag_code = 'br'
    elif lang_code == 'en':
        flag_code = 'gb'
    else:
        flag_code = ''
    return flag_code