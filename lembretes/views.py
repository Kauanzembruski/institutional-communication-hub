from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import Lembrete
from datetime import date
import json
from apps.core.decorators.ratelimit import upload_rate_limit, excluir_rate_limit



@login_required
def tela_lembretes(request):

    lembretes = Lembrete.objects.all()

    titulo = request.GET.get('titulo', '').strip()
    data = request.GET.get('data', '').strip()

    if titulo:
        lembretes = lembretes.filter(
            titulo_lembrete__icontains=titulo
        )

    if data:
        lembretes = lembretes.filter(
        data_expi__gte=data
    )


    lembretes = lembretes.order_by('-data_publi')

    return render(
        request,
        'admin/lembretesadm.html',
        {
            'lembretes': lembretes,
            'titulo': titulo,
            'data': data
        }
    )

@login_required
@upload_rate_limit
def criar_lembrete(request):

    if request.method == 'POST':

        dados = json.loads(request.body)

        # VALIDAÇÃO
        if dados['data'] < date.today().isoformat():

            return JsonResponse({

                'erro': 'Não é permitido cadastrar lembretes com data anterior à atual.'

            }, status=400)

        lembrete = Lembrete.objects.create(

            titulo_lembrete=dados['titulo'],

            conteudo_lembrete=dados['descricao'],

            data_expi=dados['data']

        )

        return JsonResponse({

            'id': lembrete.id_lembrete,

            'titulo': lembrete.titulo_lembrete,

            'descricao': lembrete.conteudo_lembrete,

            'data': str(lembrete.data_expi)

        })

    return JsonResponse({

        'erro': 'Método inválido'

    })


@login_required
@upload_rate_limit
def editar_lembrete(request, id):

    lembrete = get_object_or_404(
        Lembrete,
        id_lembrete=id
    )

    if request.method == 'POST':

        dados = json.loads(request.body)

        if dados['data'] < date.today().isoformat():

            return JsonResponse({
                'erro': 'Não é permitido informar uma data anterior à atual.'
            }, status=400)

        lembrete.conteudo_lembrete = dados['descricao']
        lembrete.data_expi = dados['data']

        lembrete.save()

        return JsonResponse({
            'status': 'ok',
            'data': str(lembrete.data_expi)
        })


@login_required
@excluir_rate_limit
def excluir_lembrete(request, id):

    lembrete = get_object_or_404(

        Lembrete,

        id_lembrete=id

    )

    lembrete.delete()

    return JsonResponse({

        'status': 'ok'

    })