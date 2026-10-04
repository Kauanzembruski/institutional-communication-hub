from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.tela_cardapio,
        name='cardapio'
    ),



    path(
        'editar/<int:id>/',
        views.editar_cardapio,
        name='editar_cardapio'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_cardapio,
        name='excluir_cardapio'
    ),



    path(
        'cardapioPublico/',
        views.tela_cardapio_tv,
        name='cardapio_tv'
    ),

]