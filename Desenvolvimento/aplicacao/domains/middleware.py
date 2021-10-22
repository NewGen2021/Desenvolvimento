from django.utils.deprecation import MiddlewareMixin
import sys
from threading import local
from domains.models import Domain
from django.core.exceptions import FieldDoesNotExist, ObjectDoesNotExist
from django.conf import settings

local_global = local()

def create_simple_domains_for_test():
        Domain.objects.get_or_create(
            domain = "newgenapp.link",
            name = "newgen",
            isActive = True)
        Domain.objects.get_or_create(
            domain = "coworking.com",
            name = "coworking",
            isActive = True)

class CurrentDomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.domain = {}
        from .models import Domain

        if settings.AUTOMATIC_TEST:
            create_simple_domains_for_test()
            from tests.conf_tests import tests_local as tl
            if hasattr(tl, 'current_app'):
                if (tl.current_app == 'gere_coworking'):
                    request.domain['domain'] = Domain.objects.get(name="coworking")
                    request.domain['isActive'] = True
                    return
                if (tl.current_app == 'cria_coworking'):
                    request.domain['domain'] = Domain.objects.get(name="newgen")
                    request.domain['isActive'] = True
                    return
            
            request.domain['domain'] = None
            request.domain['isActive'] = False
            return

        request.domain['domain'] = Domain.objects.get_current(request)
        if request.domain['domain'] is None:
            request.domain['isActive'] = False
        else:
            request.domain['isActive'] = Domain.objects.get_active(request)

class GetMatchingDatabase(MiddlewareMixin):
    def process_request(self, request):
        if settings.AUTOMATIC_TEST:
            return
        
        dominio_id = Domain.objects.using('default').filter(domain=request.domain['domain'])[0].id
        from cria_coworking.models import Administrador
        try:
            database = Administrador.objects.using('default').get(domain=dominio_id).database
        except ObjectDoesNotExist:
            database = 'default'
        local_global.database_name = database



# class RouterMiddleware (object):

#     def process_view( self, request, view_func, args, kwargs ):
#         # Check the user logged in
#         user = self.request.user
#         # Call your functions to set the database by passing the user.id



#     def process_response( self, request, response ):
#         # Make the database to default here if you wish to use it no longer

#         return response
