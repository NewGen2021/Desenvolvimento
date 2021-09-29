from cria_coworking.views import apresentacao
from django.contrib import admin
from django.urls import path, include
from cria_coworking.views import *


urlpatterns = [
    path('apresentacao', apresentacao, name="apresentacao"),
    path('cadastrar_coworking', cadastrar_coworking, name="cadastrar_coworking"),
]
