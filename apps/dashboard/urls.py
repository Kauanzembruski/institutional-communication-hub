from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [


    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'login/',
        views.index,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    path(
        'painel/',
        views.painel,
        name='painel'
    ),

    

    path(
        'eventosadm/',
        views.eventosadm,
        name='eventosadm'
    ),


    path(
        'pxaulasadm/',
        views.pxaulasadm,
        name='pxaulasadm'
    ),

        path(
        'cardapio/',
        include('cardapio.urls')
    ),

    path(
        'pxaulas/',
        include('pxaulas.urls')
    ),
 path(
        "esqueci-senha/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/home/esqueci-senha/enviado/"
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
            success_url="/home/redefinir-senha/concluido/"
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
   path(
        'horario-servidor/',
        views.horario_servidor,
        name='horario_servidor',
    ),


   ]

