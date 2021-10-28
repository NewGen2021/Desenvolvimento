# application related urls

from django.contrib import admin
from django.urls import path, include
#from django.contrib.auth import views as auth_views
from gere_coworking.views.views import home, escolherCadastro, loginUser, loginSystem, registrarUsuario, registrarFuncionario, registrarAdministrador
from gere_coworking.views.views import agendamento, index, reserva, listarReservas, menuAdmin, customizacao, emProducao, loginNovo
from gere_coworking.views.views import listarReservasIndex, base_html

urlpatterns = [
    path('home', home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('accounts/escolherCadastro', escolherCadastro, name='escolherCadastro'),
    path('accounts/loginUser', loginUser, name='loginUser'),
    path('accounts/loginSystem', loginSystem, name='loginSystem'),
    path('accounts/loginNovo', loginNovo, name='loginNovo'),
    path('accounts/registrarUsuario', registrarUsuario, name='registrarUsuario'),
    path('accounts/registrarFuncionario', registrarFuncionario, name='registrarFuncionario'),
    path('accounts/registrarAdmin', registrarAdministrador, name='registrarAdmin'),
    path('agendamento/<int:id_tipo_espaco>', agendamento, name="agendamento"),
    path('reserva', reserva, name="reserva"),
    path('listarReservas', listarReservas, name="listarReservas"),
    path('listarReservasIndex', listarReservasIndex, name="listarReservasIndex"),
    path('', index, name="index"),
    path('menuAdmin', menuAdmin, name="menuAdmin"),
    path('customizacao', customizacao, name='customizacao'),
    path('emProducao', emProducao, name="emProducao"),
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password"), name="reset_password"),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('base', base_html, name='baseHtml')
    

]
