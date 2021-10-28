from cria_coworking.views import index
from django.contrib import admin
from django.urls import path, include
from cria_coworking.views import *
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('cadastrar_coworking', cadastrar_coworking, name="cadastrar_coworking"),
    path('registrarAdmin', registrarAdministrador, name='registrarAdmin'),
]

lista_aux = []
for urlp in urlpatterns:
    lista_aux += i18n_patterns(urlp)

urlpatterns += lista_aux
