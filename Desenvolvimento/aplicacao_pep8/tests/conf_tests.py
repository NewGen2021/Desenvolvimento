import json, sys
from django.conf import settings
from importlib import reload
from django.urls import clear_url_caches
from functools import wraps
from threading import local

tests_local = local()
def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        clear_url_caches()
        reload(sys.modules[settings.ROOT_URLCONF])

def selecionar_app(app):
    def inner(test):
        @wraps(test)
        def wrapper(*args, **kwargs):
            tests_local.current_app = app
            reload_urlconf()
            return test(*args, **kwargs)
        return wrapper
    return inner    