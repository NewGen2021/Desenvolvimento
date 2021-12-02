from os import name
from django.conf.urls.static import static
from django.conf.urls import url

from cria_coworking.views import index
from django.contrib import admin
from django.urls import path, include
from cria_coworking.views import *
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib.auth import views as auth_views
import sys

urlpatterns = [
    path('', index, name="index_cria"),
    # path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('registrarAdmin', registrarAdministrador, name='registrarAdmin'),
    path('accounts/loginSystem', loginNewGen, name='loginNewgen'),
    path('assinatura', assinatura, name='assinatura'),
    path('gerenciar_plano', gerenciar_plano, name='gerenciar_plano'),
    path('pagar_plano', pagar_plano, name='pagar_plano'),
    path('registrarCoworking', registrarCoworking, name='registrarCoworking'),
    path('registrarContaNaInstancia', registrarContaNaInstancia, name='registrarContaNaInstancia'),
    path('password_reset/', CustomPasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('', include('rest_api.urls')),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if not settings.AUTOMATIC_TEST:

    lista_aux = []
    for urlp in urlpatterns:
        lista_aux += i18n_patterns(urlp)

    urlpatterns += lista_aux

