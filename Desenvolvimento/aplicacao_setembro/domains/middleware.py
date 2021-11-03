from django.utils.deprecation import MiddlewareMixin
import sys
from threading import local
from domains.models import Domain
from django.core.exceptions import ObjectDoesNotExist

local_global = local()

class CurrentDomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        from .models import Domain
        request.domain = {}
        request.domain['domain'] = Domain.objects.get_current(request)
        if request.domain['domain'] is None:
            request.domain['isActive'] = False
        else:
            request.domain['isActive'] = Domain.objects.get_active(request)

class CustomerMiddleware(MiddlewareMixin):
    def process_request(self, request):
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
