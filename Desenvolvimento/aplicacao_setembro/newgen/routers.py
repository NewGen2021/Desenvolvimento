from domains.middleware import local_global
import sys

class DataBaseRouter(object):

    def db_for_read(self, model, **hints):
        # user = self.request.user
        # if user.id == 1:
        #     return "master"
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", file=sys.stderr)
        print(model, file=sys.stderr)
        print(model._meta.app_label, file=sys.stderr)
        print(model._meta, file=sys.stderr)
        db = 'default'
        if hasattr(local_global, 'database_name'):
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", file=sys.stderr)
            print(local_global.database_name, file=sys.stderr)
            db = local_global.database_name
        # print(hints.request, file=sys.stderr)
        return db

    def db_for_write(self, model, **hints):
        # user = self.request.user
        # if user.id == 1:
        #     return "master"
        db = 'default'
        if hasattr(local_global, 'database_name'):
            db = local_global.database_name
        return db
    
    def allow_relation(self, obj1, obj2, **hints):
	    # if (obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels):
		#     return True
	    return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
    #     pass
	# def allow_migrate(self, db, app_label, model_name=None, **hints):
	#     if app_label in self.route_app_labels:
	# 	    return db == 'users_db'
	#     return None
