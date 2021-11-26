import json
from django.conf import settings

def json_to_safe_html_string(d: dict):
    return str(json.dumps(d)).replace("{", '&#x7B;').replace('}', '&#x7D;')

def get_available_languages() -> list:
    available_languages = []
    for lang_tuple in settings.LANGUAGES:
        available_languages.append(lang_tuple[0])
    return available_languages

def get_default_language_if_language_code_doesnt_exist(lang_code: str) -> str:
    languages = get_available_languages()
    if lang_code not in languages:
        return settings.LANGUAGE_CODE
    return lang_code