from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.calendario,
        name='calendario'
    ),

    path(
        'calendarioPublico/',
        views.calendario_publico,
        name='calendario_publico'
    ),

    path(
        'criar/',
        views.criar_prova,
        name='criar_prova'
    ),

    path(
        'editar/<int:id>/',
        views.editar_prova,
        name='editar_prova'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_prova,
        name='excluir_prova'
    ),

]