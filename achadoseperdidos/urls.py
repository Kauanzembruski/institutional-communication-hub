from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.achados,
        name='achados'
    ),

    path(
    'achadosPublico/',
    views.achados_publico,
    name='achados_publico'
    ),
    path(
        'criar/',
        views.criar_item,
        name='criar_item'
    ),

    path(
        'editar/<int:id>/',
        views.editar_item,
        name='editar_item'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_item,
        name='excluir_item'
    ),

]