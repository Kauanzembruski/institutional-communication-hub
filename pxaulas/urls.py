from django.urls import path
from . import views

urlpatterns = [

    path("horarios/", views.tela_horarios, name="horarios"),

    path(
        "listar_horarios/",
        views.listar_horarios,
        name="listar_horarios"
    ),

   path(
    "proximas-aulas/<str:curso>/",
    views.pxaulas_publico,
    name="pxaulasPublico"
),

path(
    "api/proximas-aulas/<str:curso>/",
    views.proximas_aulas,
    name="proximas_aulas"
),
    path(
    "proximas_aulas/",
    views.proximas_aulas,
    name="proximas_aulas"
    ),
    
    path(
        "criar_horario/",
        views.criar_horario,
        name="criar_horario"
    ),

    path(
        "editar_horario/",
        views.editar_horario,
        name="editar_horario"
    ),

    path(
        "excluir_horario/",
        views.excluir_horario,
        name="excluir_horario"
    ),
]