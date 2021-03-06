from domains.middleware import local_global
import sys

class DataBaseRouter(object):

    def db_for_read(self, model, **hints):
        db = 'default'
        if hasattr(local_global, 'database_name'):
            db = local_global.database_name
        return db

    def db_for_write(self, model, **hints):
        db = 'default'
        if hasattr(local_global, 'database_name'):
            db = local_global.database_name
        return db
    
    def allow_relation(self, obj1, obj2, **hints):
	    return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
