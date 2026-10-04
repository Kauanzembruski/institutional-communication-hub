from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date
from .models import Prova
import calendar
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import Aviso, Dataimpor
from apps.core.decorators.ratelimit import upload_rate_limit, excluir_rate_limit

def calendario_publico(request):

    hoje = date.today()

    ano = int(
        request.GET.get(
            'ano',
            hoje.year
        )
    )

    mes = int(
        request.GET.get(
            'mes',
            hoje.month
        )
    )

    quinzena = int(
        request.GET.get(
            'quinzena',
            1
        )
    )

    ultimo_dia = calendar.monthrange(
        ano,
        mes
    )[1]


    # =========================
    # DEFINE A QUINZENA
    # =========================

    if quinzena == 1:

        dia_inicio = 1
        dia_fim = 14

    else:

        dia_inicio = 15
        dia_fim = ultimo_dia


    # =========================
    # PROVAS
    # =========================

    provas = Prova.objects.filter(

        data__year=ano,

        data__month=mes,

        data__day__gte=dia_inicio,

        data__day__lte=dia_fim

    ).order_by(
        'data'
    )


    # =========================
    # DATAS IMPORTANTES
    # =========================

    datas_importantes = Dataimpor.objects.filter(

        data__year=ano,

        data__month=mes,

        data__day__gte=dia_inicio,

        data__day__lte=dia_fim

    )


    datas_importantes_dict = {

        item.data.strftime('%Y-%m-%d'): item

        for item in datas_importantes

    }


    # =========================
    # DIAS DO CALENDÁRIO
    # =========================

    dias_periodo = []


    for dia in range(
        dia_inicio,
        dia_fim + 1
    ):

        data_completa = date(
            ano,
            mes,
            dia
        )


        data_key = data_completa.strftime(
            '%Y-%m-%d'
        )


        data_importante = (
            datas_importantes_dict.get(
                data_key
            )
        )


        coluna_semana = (
            data_completa.weekday() + 1
        )


        dias_periodo.append({

            'numero': dia,

            # mantém a string para comparações
            'data': data_key,

            # NOVO
            'coluna_semana': coluna_semana,

            'data_importante':
                data_importante,

        })


    datas_importantes_lista = list(
        datas_importantes_dict.keys()
    )


    # =========================
    # PROVAS PARA O TEMPLATE
    # =========================

    provas_periodo = []

    provas_por_dia = {}


    for prova in provas:

        chave = prova.data.strftime(
            '%Y-%m-%d'
        )


        prova_dict = {

            'data':
                prova.data.strftime('%d/%m'),

            'turma':
                prova.turma,

            'disciplina':
                prova.disciplina

        }


        provas_periodo.append(
            prova_dict
        )


        provas_por_dia.setdefault(
            chave,
            []
        ).append(
            prova_dict
        )


    # =========================
    # AVISOS
    # =========================

    avisos = Aviso.objects.filter(

        status_aviso='ativo',

        data_publi__lte=hoje,

        data_expi__gte=hoje

    ).order_by(
        '-data_publi'
    )[:5]


    return render(

        request,

        'provas.html',

        {

            'dias_periodo':
                dias_periodo,

            'hoje':
                hoje.strftime('%Y-%m-%d'),

            'datas_importantes_lista':
                datas_importantes_lista,

            'provas_periodo':
                provas_periodo,

            'provas_por_dia':
                provas_por_dia,

            'quinzena':
                quinzena,

            'mes':
                mes,

            'ano':
                ano,

            'avisos':
                avisos

        }

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
@upload_rate_limit
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
@upload_rate_limit
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
@excluir_rate_limit
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