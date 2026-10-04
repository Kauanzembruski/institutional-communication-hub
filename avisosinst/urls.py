from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.avisos,
        name='avisosinst'
    ),

    path(
        'criar/',
        views.criar_aviso,
        name='criar_aviso'
    ),

    path(
        'editar/<int:id>/',
        views.editar_aviso,
        name='editar_aviso'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_aviso,
        name='excluir_aviso'
    ),

]