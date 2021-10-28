# application related urls

from django.contrib import admin
from django.urls import path, include
from gere_coworking.views.views import (
    home, escolherCadastro, loginUser, loginSystem, registrarUsuario, registrarFuncionario, 
    registrarAdministrador, agendamento, index, reserva, listarReservas, menuAdmin, customizacao, 
    emProducao, loginNovo,listarReservasIndex, base_html, teste, form_teste, form_teste2, form_pagamento)

from django.contrib.auth import views as auth_views


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
    path('pagamento', form_pagamento, name="pagamento"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
   ]
