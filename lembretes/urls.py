from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.tela_lembretes,
        name='lembretes'
    ),

    path(
        'criar/',
        views.criar_lembrete,
        name='criar_lembrete'
    ),

    path(
        'editar/<int:id>/',
        views.editar_lembrete,
        name='editar_lembrete'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_lembrete,
        name='excluir_lembrete'
    ),

]