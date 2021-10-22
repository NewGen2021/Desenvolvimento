from django.contrib import admin
from django.urls import path, include
# from gere_coworking.views.views import (
#     home, escolherCadastro, loginUser, loginSystem, registrarUsuario, registrarFuncionario, 
#     registrarAdministrador, agendamento, index, reserva, listarReservas, menuAdmin, customizacao, 
#     emProducao, loginNovo,listarReservasIndex, base_html, teste, form_teste, form_teste2, form_pagamento, CustomPasswordResetView,
#     CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView   )
from gere_coworking.views.views import *
from django.contrib.auth import views as auth_views
from rest_api.router import router
from rest_api.viewsets import *


urlpatterns = [
    path('home', home, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('', index, name="index"),
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
    path('menuAdmin', menuAdmin, name="menuAdmin"),
    path('customizacao', customizacao, name='customizacao'),
    path('emProducao', emProducao, name="emProducao"),
    path('base', base_html, name='baseHtml'),
    path('teste', teste, name="teste"),
    path('form/teste', form_teste, name="form_teste"),
    path('form/teste2', form_teste2, name="form_teste"),
    path('pagamento_reserva/<int:id_reserva>', form_pagamento, name="pagamento_reserva"),
    path('password_reset/', CustomPasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('teste', teste, name="teste"),
    path('listar_espacos', listar_espacos, name="listar_espacos"),
    path('editar_tipo_espaco/<int:id_tipo_espaco>/', editar_tipo_espaco, name="editar_tipo_espaco"),
    path('editar_espaco/<int:id_espaco>', editar_tipo_espaco, name="editar_tipo_espaco"),
   ]
