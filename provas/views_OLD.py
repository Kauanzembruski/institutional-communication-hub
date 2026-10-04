from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
import calendar
from .models import Prova
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import Aviso


def calendario_publico(request):

    hoje = date.today()

    ano = hoje.year
    mes = hoje.month

    provas = Prova.objects.filter(
        data__year=ano,
        data__month=mes
    ).order_by('data')

    provas_por_dia = {}

    for prova in provas:

        dia = prova.data.day

        if dia not in provas_por_dia:

            provas_por_dia[dia] = []

        provas_por_dia[dia].append({

            'turma': prova.turma,
            'disciplina': prova.disciplina

        })

    avisos = Aviso.objects.filter(
        status_aviso='ativo',
        data_expi__gte=date.today()
    ).order_by('-data_publi')[:5]

    contexto = {

        'dias_mes': range(
            1,
            calendar.monthrange(ano, mes)[1] + 1
        ),

        'mes': mes,
        'ano': ano,

        'hoje': hoje.day,

        'provas_por_dia': provas_por_dia,

        'avisos': avisos

    }

    return render(
        request,
        'provas.html',
        contexto
    )


@login_required
def calendario(request):

    provas = Prova.objects.all()

    disciplina = request.GET.get('disciplina')
    data = request.GET.get('data')
    curso = request.GET.get('curso')

    if curso:
        provas = provas.filter(
            curso__icontains=curso
        )
    
    if disciplina:
        provas = provas.filter(
            disciplina__icontains=disciplina
        )

    if data:
        provas = provas.filter(
            data__gte=data
        )

    provas = provas.order_by(
        'curso',
        'data'
    )

    contexto = {
        'provas': provas,
        'hoje': date.today().isoformat(),
        'disciplina': disciplina,
        'data': data,
    }

    return render(
        request,
        'admin/calendarioprovaadm.html',
        contexto
    )

@login_required
def criar_prova(request):

    if request.method == 'POST':

        data = request.POST.get('data')

        if data < date.today().isoformat():

            messages.error(
                request,
                'Não é permitido cadastrar provas com datas anteriores.'
            )

            return redirect('calendario')

        Prova.objects.create(

            curso=request.POST.get('curso'),

            disciplina=request.POST.get('disciplina'),

            turma=request.POST.get('turma'),

            data=data

        )

        messages.success(
            request,
            'Prova cadastrada com sucesso.'
        )

    return redirect('calendario')


@login_required
def editar_prova(request, id):

    prova = get_object_or_404(
        Prova,
        id=id
    )

    if request.method == 'POST':

        nova_data = request.POST.get('data')

        if nova_data < date.today().isoformat():

            messages.error(
                request,
                'A data não pode ser inferior à atual.'
            )

            return redirect('calendario')

        prova.curso = request.POST.get('curso')
        prova.turma = request.POST.get('turma')
        prova.disciplina = request.POST.get('disciplina')
        prova.data = nova_data

        prova.save()

        messages.success(
            request,
            'Prova atualizada com sucesso.'
        )

    return redirect('calendario')

@login_required
def excluir_prova(request, id):

    prova = get_object_or_404(
        Prova,
        id=id
    )

    prova.delete()

    messages.success(
        request,
        'Prova excluída com sucesso.'
    )

    return redirect('calendario')