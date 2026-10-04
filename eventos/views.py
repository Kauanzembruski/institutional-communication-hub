from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from apps.dashboard.models import Evento, Aviso
from apps.core.decorators.ratelimit import (
    upload_rate_limit,
    excluir_rate_limit
)


def eventos_publico(request):

    hoje = date.today()

    eventos = Evento.objects.filter(
        data_fim__gte=hoje
    ).order_by(
        "data_inicio",
        "hora_inicio"
    )

    avisos = Aviso.objects.filter(
        status_aviso='ativo',
        data_publi__lte=hoje,
        data_expi__gte=hoje
    ).order_by('-data_publi')[:5]

    return render(
        request,
        "eventos.html",
        {
            "eventos": eventos,
            "avisos": avisos
        }
    )


@login_required
def eventosadm(request):

    eventos = Evento.objects.all().order_by(
        "-id_evento"
    )

    titulo = request.GET.get('titulo')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if titulo:
        eventos = eventos.filter(
            titulo__icontains=titulo
        )

    if data_inicio:
        eventos = eventos.filter(
            data_inicio__gte=data_inicio
        )

    if data_fim:
        eventos = eventos.filter(
            data_fim__lte=data_fim
        )

    return render(
        request,
        "admin/eventosadm.html",
        {
            "eventos": eventos,
            "hoje": date.today().isoformat()
        }
    )


@login_required
@upload_rate_limit
def criar_evento(request):

    if request.method == "POST":

        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        data_inicio = request.POST.get("data_inicio")
        data_fim = request.POST.get("data_fim")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fim = request.POST.get("hora_fim")
        imagem = request.FILES.get("imagem")

        if data_inicio < date.today().isoformat():

            return JsonResponse({
                "erro":
                    "Não é permitido criar eventos em datas passadas."
            }, status=400)

        if data_fim < data_inicio:

            return JsonResponse({
                "erro":
                    "A data final não pode ser menor que a inicial."
            }, status=400)

        if (
            data_inicio == data_fim
            and hora_fim <= hora_inicio
        ):

            return JsonResponse({
                "erro":
                    "O horário final não pode ser menor ou igual ao inicial."
            }, status=400)

        evento = Evento.objects.create(
            titulo=titulo,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            imagem=imagem
        )

        return JsonResponse({
            "status": "ok",
            "id": evento.id_evento
        })

    return JsonResponse(
        {"erro": "Método inválido"},
        status=405
    )


@login_required
@upload_rate_limit
def editar_evento(request, id):

    evento = get_object_or_404(
        Evento,
        id_evento=id
    )

    if request.method == "POST":

        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        data_inicio = request.POST.get("data_inicio")
        data_fim = request.POST.get("data_fim")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fim = request.POST.get("hora_fim")
        imagem = request.FILES.get("imagem")

        if data_inicio < date.today().isoformat():

            return JsonResponse({
                "erro":
                    "Não é permitido salvar eventos em datas passadas."
            }, status=400)

        if data_fim < data_inicio:

            return JsonResponse({
                "erro":
                    "A data final não pode ser menor que a inicial."
            }, status=400)

        if (
            data_inicio == data_fim
            and hora_fim <= hora_inicio
        ):

            return JsonResponse({
                "erro":
                    "O horário final não pode ser menor ou igual ao inicial."
            }, status=400)

        evento.titulo = titulo
        evento.descricao = descricao
        evento.data_inicio = data_inicio
        evento.data_fim = data_fim
        evento.hora_inicio = hora_inicio
        evento.hora_fim = hora_fim

        if imagem:
            evento.imagem = imagem

        evento.save()

        return JsonResponse({
            "status": "ok"
        })

    return JsonResponse(
        {"erro": "Método inválido"},
        status=405
    )


@login_required
@excluir_rate_limit
def excluir_evento(request, id):

    evento = get_object_or_404(
        Evento,
        id_evento=id
    )

    evento.delete()

    return JsonResponse({
        "status": "ok"
    })