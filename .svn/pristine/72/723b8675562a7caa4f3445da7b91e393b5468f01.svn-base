from domains.middleware import local_global
from threadlocals.threadlocals import get_current_request
from domains import domain_manager
import sys


class DataBaseRouter(object):

    def db_for_read(self, model, **hints):
        db = 'default'
        if model._meta.app_label in ['custom_templates', 'cria_coworking']:
            return db
        # if hasattr(local_global, 'database_name'):
        #     db = local_global.database_name
        # return db
        return get_database_by_json(get_current_request())

    def db_for_write(self, model, **hints):
        db = 'default'
        if model._meta.app_label in ['custom_templates', 'cria_coworking']:
            return db
        # if hasattr(local_global, 'database_name'):
        #     db = local_global.database_name
        # return db
        return get_database_by_json(get_current_request())

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

def get_database_by_json(request) -> None:
    if request is None:
        return 'default'
    domain = domain_manager.get_domain(request)
    # MUDOU TODO
    if domain is None:
        j = domain_manager.get_domain_json_or_create()
        domain = j["newgenapp.link"]
    return domain['database']
