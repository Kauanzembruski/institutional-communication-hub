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
    path(
        "esqueci-senha/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/esqueci-senha/enviado/"
        ),
        name="password_reset"
    ),

    path(
        "esqueci-senha/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),

    path(
        "redefinir-senha/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/redefinir-senha/concluido/"
        ),
        name="password_reset_confirm"
    ),

    path(
        "redefinir-senha/concluido/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),


]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )