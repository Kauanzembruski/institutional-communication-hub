from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        eventosadm,
        name="eventosadm"
    ),

    path(
    "eventosPublico/",
    eventos_publico,
    name="eventos_publico"
),



    path(
        "criar/",
        criar_evento,
        name="criar_evento"
    ),

    path(
        "editar/<int:id>/",
        editar_evento,
        name="editar_evento"
    ),

    path(
        "excluir/<int:id>/",
        excluir_evento,
        name="excluir_evento"
    ),

]