from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from apps.dashboard.models import Dataimpor
from django.contrib.auth.decorators import login_required
from .forms import DataimporForm
from apps.core.decorators.ratelimit import upload_rate_limit

@login_required
# Página do calendário
def calendario(request):

    datas = Dataimpor.objects.all()

    data_json = []

    for data in datas:
        data_json.append({
            'id': data.id,
            'titulo': data.titulo,
            'descricao': data.descricao,
            'data': data.data.strftime('%Y-%m-%d')
        })

    return render(request, 'admin/datasimpoadm.html', {
        'datas': data_json
    })


# Salvar datas
@login_required
@upload_rate_limit
def salvar_data(request):

    if request.method == 'POST':

        form = DataimporForm(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


# Editar datas
@login_required
def editar_data(request, data_id):

    data = get_object_or_404(Dataimpor, id=data_id)

    if request.method == 'POST':

        form = DataimporForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


# Excluir datas
@login_required
def excluir_data(request, data_id):

    data = get_object_or_404(Dataimpor, id=data_id)

    data.delete()

    return JsonResponse({
        'success': True
    })