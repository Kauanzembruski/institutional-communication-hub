from datetime import date, datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import Aviso, InformacaoOperacional, Dataimpor
from django.views.decorators.csrf import csrf_exempt
from apps.dashboard.utils import obter_clima
import json
from apps.core.decorators.ratelimit import upload_rate_limit, excluir_rate_limit


def info_publico(request):

    hoje = date.today()

    infos = InformacaoOperacional.objects.filter(
        data_lancamento__gte=hoje
    ).order_by(
        "data_lancamento"
    )

    meses = {
        1: 'JANEIRO',
        2: 'FEVEREIRO',
        3: 'MARÇO',
        4: 'ABRIL',
        5: 'MAIO',
        6: 'JUNHO',
        7: 'JULHO',
        8: 'AGOSTO',
        9: 'SETEMBRO',
        10: 'OUTUBRO',
        11: 'NOVEMBRO',
        12: 'DEZEMBRO'
    }

    mes_atual_numero = datetime.now().month
    mes_atual = meses[mes_atual_numero]

    avisos = Aviso.objects.filter(
        status_aviso='ativo',
        data_publi__lte=hoje,
        data_expi__gte=hoje
    ).order_by('-data_publi')[:5]

    datas_importantes = (
        Dataimpor.objects
        .filter(
            data__month=mes_atual_numero
        )
        .order_by('data')
    )

    clima = obter_clima()

    return render(
        request,
        "infoop.html",
        {
            "infos": infos,
            "avisos": avisos,
            "datas_importantes": datas_importantes,
            "mes_atual": mes_atual,
            "clima": clima
        }
    )

# LISTAR
@login_required
def infoopadm(request):

    infos = InformacaoOperacional.objects.all()

    titulo = request.GET.get('titulo')
    data = request.GET.get('data')
    categoria = request.GET.get('categoria')

    if titulo:

        infos = infos.filter(
            titulo__icontains=titulo
        )

    if data:

        infos = infos.filter(
        data_lancamento__gte=data
    )

    if categoria:

        infos = infos.filter(
            categoria=categoria
        )

    infos = infos.order_by(
        "-data_lancamento"
    )

    return render(

        request,

        "admin/infoopadm.html",

        {

            "infos": infos,

            "titulo": titulo,

            "data": data,

            "categoria": categoria

        }

    )



# CRIAR

@login_required
@upload_rate_limit
def criar_info(request):

    if request.method == "POST":

        dados = json.loads(request.body)

        InformacaoOperacional.objects.create(

            data_lancamento=dados["data"],

            titulo=dados["titulo"],

            categoria=dados["categoria"]

        )

        return JsonResponse({

            "status":"ok"

        })


# EDITAR

@login_required
@upload_rate_limit
def editar_info(request, id):

    if request.method == "POST":

        dados = json.loads(request.body)

        info = InformacaoOperacional.objects.get(
            id_info=id
        )

        info.data_lancamento = dados["data"]

        info.titulo = dados["titulo"]

        info.categoria = dados["categoria"]

        info.save()

        return JsonResponse({

            "status":"ok"

        })


# EXCLUIR

@login_required
@excluir_rate_limit
def excluir_info(request, id):

    if request.method == "POST":

        info = InformacaoOperacional.objects.get(
            id_info=id
        )

        info.delete()

        return JsonResponse({

            "status":"ok"

        })