from datetime import date
from apps.core.ciclos import obter_ciclo
from .models import Aviso, Lembrete, Evento, InformacaoOperacional, Dataimpor, Cardapio
from achadoseperdidos.models import ItemAchado
from provas.models import Prova
from pxaulas.views import obter_proximas_aulas
from cardapio.views import DIAS_CARDAPIO
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .utils import obter_clima
from apps.core.decorators.ratelimit import login_rate_limit
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.cache import never_cache


@never_cache
def horario_servidor(request):
    return JsonResponse({
        "timestamp": timezone.now().timestamp() * 1000,
        "fuso": settings.TIME_ZONE,
    })

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
    hoje = date.today()
    quinzena = 1 if hoje.day <= 14 else 2
    periodo = {
        'data__year': hoje.year,
        'data__month': hoje.month,
        'data__day__gte': 1 if quinzena == 1 else 15,
        'data__day__lte': 14 if quinzena == 1 else 31,
    }
    avisos = Aviso.objects.filter(
        status_aviso='ativo',
        data_publi__lte=hoje,
        data_expi__gte=hoje,
    ).order_by('-data_publi')[:5]
    contexto = {
        'ciclo': obter_ciclo(request),
        'avisos': avisos,
        'clima': obter_clima(),
        'tem_eventos': Evento.objects.filter(data_fim__gte=hoje).exists(),
        'tem_lembretes': Lembrete.objects.filter(data_expi__gte=hoje).exists(),
        'tem_achados': ItemAchado.objects.exists(),
        'tem_infos': (
            InformacaoOperacional.objects.filter(data_lancamento__gte=hoje).exists()
            or Dataimpor.objects.filter(data__month=hoje.month).exists()
        ),
        'tem_calendario': (
            Prova.objects.filter(**periodo).exists()
            or Dataimpor.objects.filter(**periodo).exists()
        ),
        'quinzena': quinzena,
        'tem_cardapio': any(
            (lanche or '').strip() not in ('', '-')
            for lanche in Cardapio.objects.filter(
                dia_semana__in=DIAS_CARDAPIO
            ).values_list('lanche', flat=True)
        ),
    }
    for curso in ('TII', 'ADM', 'ADS', 'TPG'):
        contexto[f'tem_aulas_{curso.lower()}'] = bool(
            obter_proximas_aulas(curso)['dados']
        )
    return render(request, 'PainelPublico.html', contexto)


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


