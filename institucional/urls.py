from django.contrib import admin
from django.urls import path, include

from apps.dashboard import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'home/',
        include('apps.dashboard.urls')
    ),
    
        path(
        '',
        views.painel_publico,
        name='painel_publico'
    ),

    path(
        'lembretes/',
        include('lembretes.urls')
    ),

    path(
        'cardapio/',
        include('cardapio.urls')
    ),
    path(
        'lembretePublico/',
        views.tela_tv,
        name='tv'
    ),
    path(
        'provas/',
        include('provas.urls')
    ), 
    
    path(
        'achadoseperdidos/',
        include('achadoseperdidos.urls')
    ),

    path(
    'avisoinstadm/',
    include('avisosinst.urls')
    ),
    path('pxaulas/', include('pxaulas.urls')),
    
    path(
    "eventos/",
    include("eventos.urls")
),

path(
    "infoopadm/",
    include("infop.urls")
),
path(
    "infoop/",
    include("infop.urls")
),

    path(
        'datasimport/',
        include('datasimport.urls')
    ),

]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )