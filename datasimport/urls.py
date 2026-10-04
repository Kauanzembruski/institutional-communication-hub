from django.urls import path
from . import views


urlpatterns = [

    
    path(
        '',
        views.calendario,
        name='datasimport'
    ),

    path(
        'salvar-data/',
        views.salvar_data,
        name='salvar_data'
    ),

    path(
        'editar-data/<int:data_id>/',
        views.editar_data,
        name='editar_data'
    ),

    path(
        'excluir-data/<int:data_id>/',
        views.excluir_data,
        name='excluir_data'
    ),
]