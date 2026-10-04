from datetime import date
from .models import Aviso, Lembrete, Evento
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .utils import obter_clima
from apps.core.decorators.ratelimit import login_rate_limit

@login_rate_limit
def index(request):

    erro = None

    if request.method == "POST":

        email = request.POST.get("email")

        senha = request.POST.get("senha")

        try:

            usuario = User.objects.get(email=email)

            if usuario.check_password(senha):

                auth_login(request, usuario)

                return redirect("painel")

            else:

                erro = "Senha inválida"

        except User.DoesNotExist:

            erro = "E-mail não encontrado"

    return render(
        request,
        "index.html",
        {
            "erro": erro
        }
    )

def logout_view(request):

    logout(request)

    return redirect('index')





def tela_tv(request):

    hoje = date.today()

    lembretes = Lembrete.objects.filter(
        data_expi__gte=hoje
    ).order_by("data_expi")

    avisos = Aviso.objects.filter(
        status_aviso='ativo',
        data_publi__lte=hoje,
        data_expi__gte=hoje
    ).order_by('-data_publi')[:5]

    return render(
        request,
        'lembretes.html',
        {
            'lembretes': lembretes,
            'avisos': avisos
        }
    )


def painel_publico(request):

    avisos = Aviso.objects.filter(
        status_aviso='ativo',
        data_expi__gte=date.today()
    ).order_by('-data_publi')[:5]

    clima = obter_clima()

    return render(
        request,
        'PainelPublico.html',
        {
            'avisos': avisos,
            'clima': clima,
	    'tem_eventos': Evento.objects.filter(data_fim__gte=date.today()).exists(),
    	    'tem_lembretes': Lembrete.objects.filter(data_expi__gte=date.today()).exists(),
        }
    )
@login_required
def painel(request):
    return render(request, 'admin/painel.html')
@login_required
def eventosadm(request):
    return render(request, 'admin/eventosadm.html')

@login_required
def avisoinstadm(request):
    return render(request, 'admin/avisoinstadm.html')

@login_required
def pxaulasadm(request):
    return render(request, 'admin/pxaulasadm.html')
@login_required
def infoopadm(request):
    return render(request, 'admin/infoopadm.html')

from django.contrib.auth import logout
from django.shortcuts import redirect


