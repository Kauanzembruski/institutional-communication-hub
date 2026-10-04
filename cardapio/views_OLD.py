from datetime import date
import json

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.core.decorators.ratelimit import upload_rate_limit, excluir_rate_limit
from apps.dashboard.models import Cardapio, Aviso


DIAS_CARDAPIO = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-feira',
    'Sexta-feira',
    'Sábado',
]


def tela_cardapio_tv(request):
    itens = {
        item.dia_semana: item
        for item in Cardapio.objects.all()
    }

    cardapios = []

    for dia in DIAS_CARDAPIO:
        if dia in itens:
            cardapios.append(itens[dia])
        else:
            cardapios.append({
                'dia_semana': dia,
                'lanche': '-'
            })

    hoje = date.today()

    avisos = Aviso.objects.filter(
            status_aviso='ativo',
        data_publi__lte=hoje,
        data_expi__gte=hoje
    ).order_by('-data_publi')[:5]

    return render(request, 'cardapio.html', {
        'cardapios': cardapios,
        'avisos': avisos,
    })


@login_required
def tela_cardapio(request):
    itens = {
        item.dia_semana: item
        for item in Cardapio.objects.all()
    }

    cardapios = []

    for dia in DIAS_CARDAPIO:
        if dia in itens:
            cardapios.append(itens[dia])
        else:
            cardapios.append(
                Cardapio.objects.create(
                    dia_semana=dia,
                    lanche=''
                )
            )

    return render(request, 'admin/cardapioadm.html', {
        'cardapios': cardapios
    })


@login_required
@upload_rate_limit
def editar_cardapio(request, id):

    cardapio = get_object_or_404(
        Cardapio,
        id_cardapio=id
    )

    if request.method == 'POST':

        dados = json.loads(request.body)

        lanche = dados.get('lanche', '').strip()

        cardapio.lanche = lanche if lanche else '-'

        cardapio.save()

        return JsonResponse({
            'status': 'ok',
            'lanche': cardapio.lanche
        })

    return JsonResponse({
        'erro': 'Método inválido'
    }, status=405)

@login_required
@excluir_rate_limit
def excluir_cardapio(request, id):

    cardapio = get_object_or_404(

        Cardapio,

        id_cardapio=id

    )

    cardapio.delete()

    return JsonResponse({

        'status': 'ok'

    })