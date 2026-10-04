from django.core.paginator import Paginator


def obter_ciclo(request):
    valor = request.GET.get("ciclo", "0")
    # Limita a entrada e mant?m o contador seguro para o JavaScript.
    if not valor.isascii() or not valor.isdecimal() or len(valor) > 12:
        return 0
    return int(valor)


def paginar_por_ciclo(registros, ciclo, por_pagina=2):
    paginador = Paginator(registros, por_pagina)
    numero = (ciclo % paginador.num_pages) + 1
    return paginador.page(numero)
