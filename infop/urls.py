from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        infoopadm,
        name="infoopadm"
    ),

        path(

        "infoopPublico/",

        info_publico,

        name="info_publico"

    ),

    path(
        "criar/",
        criar_info
    ),

    path(
        "editar/<int:id>/",
        editar_info
    ),

    path(
        "excluir/<int:id>/",
        excluir_info
    ),

]