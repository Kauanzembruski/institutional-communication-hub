from django.contrib import admin

from provas.models import Prova

from .models import Aviso, Dataimpor, Disciplina,Permissao, Professor, Turma, Usuario, Lembrete, Cardapio, HorarioAula,Evento, InformacaoOperacional


admin.site.site_header = "Admin IFRS"
admin.site.site_title = "Admin IFRS"
admin.site.index_title = "Cadastros institucionais"
admin.site.register(Prova)

class StatusActionsMixin:
    status_field = None

    @admin.action(description="Marcar selecionados como ativo")
    def marcar_como_ativo(self, request, queryset):
        queryset.update(**{self.status_field: "ativo"})

    @admin.action(description="Marcar selecionados como inativo")
    def marcar_como_inativo(self, request, queryset):
        queryset.update(**{self.status_field: "inativo"})

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not self.status_field:
            actions.pop("marcar_como_ativo", None)
            actions.pop("marcar_como_inativo", None)
        return actions



@admin.register(Dataimpor)
class DataimporAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'criado_em')
    search_fields = ('titulo', 'descricao')
    list_filter = ('data',)


@admin.register(InformacaoOperacional)
class InformacaoOperacionalAdmin(admin.ModelAdmin):

    list_display = (
        "titulo",
        "categoria",
        "data_lancamento"
    )

    search_fields = (
        "titulo",
        "categoria"
    )

    list_filter = (
        "categoria",
        "data_lancamento"
    )

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("curso_turma", "ano_escolar", "turno_turma")
    list_filter = ("curso_turma", "ano_escolar", "turno_turma")
    search_fields = ("curso_turma", "turno_turma")
    fields = ("curso_turma", "ano_escolar", "turno_turma")
    ordering = ("curso_turma", "ano_escolar", "turno_turma")
    list_per_page = 25


@admin.register(Permissao)
class PermissaoAdmin(admin.ModelAdmin):
    list_display = ("tipo_permissao",)
    search_fields = ("tipo_permissao",)
    fields = ("tipo_permissao",)
    ordering = ("tipo_permissao",)
    list_per_page = 25

@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):

    list_display = (
        'id_lembrete',
        'titulo_lembrete',
        'data_publi',
        'data_expi',
        'fixado',
        'status',
    )

    list_filter = (
        'status',
        'fixado',
        'data_publi',
        'data_expi',
    )

    search_fields = (
        'titulo_lembrete',
        'conteudo_lembrete',
    )

    ordering = (
        '-fixado',
        '-data_publi',
    )

    list_editable = (
        'fixado',
        'status',
    )

    fieldsets = (

        ('Informações do lembrete', {
            'fields': (
                'titulo_lembrete',
                'conteudo_lembrete',
            )
        }),


        ('Datas', {
            'fields': (
                'data_expi',
            )
        }),

        ('Configurações', {
            'fields': (
                'fixado',
                'status',
            )
        }),
    )
@admin.register(Usuario)
class UsuarioAdmin(StatusActionsMixin, admin.ModelAdmin):
    status_field = "status_usu"
    list_display = ("nome", "email", "nivel_permissao", "status_usu", "ultimo_login")
    list_editable = ("status_usu",)
    list_filter = ("status_usu", "nivel_permissao")
    search_fields = ("nome", "email")
    autocomplete_fields = ("nivel_permissao",)
    readonly_fields = ("ultimo_login",)
    actions = ("marcar_como_ativo", "marcar_como_inativo")
    fieldsets = (
        ("Identificacao", {"fields": ("nome", "email", "senha")}),
        ("Vinculos", {"fields": ("nivel_permissao",)}),
        ("Status", {"fields": ("status_usu",)}),
        ("Datas", {"fields": ("data_criacao", "ultimo_login")}),
    )
    ordering = ("nome",)
    list_per_page = 25

@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = ("dia_semana", "lanche")
    list_filter = ("dia_semana",)
    search_fields = ("lanche",)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):

    list_display = (

        "id_evento",
        "titulo",
        "data_criacao"

    )

    search_fields = (

        "titulo",
        "descricao"

    )

    list_filter = (

        "data_criacao",

    )

    ordering = (

        "-id_evento",

    )

@admin.register(Disciplina)
class DisciplinaAdmin(StatusActionsMixin, admin.ModelAdmin):
    status_field = "status_disciplina"
    list_display = ("nome_disciplina", "status_disciplina")
    list_editable = ("status_disciplina",)
    list_filter = ("status_disciplina",)
    search_fields = ("nome_disciplina",)
    fields = ("nome_disciplina", "status_disciplina")
    actions = ("marcar_como_ativo", "marcar_como_inativo")
    ordering = ("nome_disciplina",)
    list_per_page = 25


@admin.register(Aviso)
class AvisoAdmin(StatusActionsMixin, admin.ModelAdmin):
    status_field = "status_aviso"
    list_display = ("titulo_aviso", "data_publi", "data_expi", "status_aviso")
    list_editable = ("status_aviso",)
    list_filter = ("status_aviso", "data_publi", "data_expi")
    search_fields = ("titulo_aviso", "mensagem")
    fields = ("titulo_aviso", "mensagem", "data_publi", "data_expi", "status_aviso")
    actions = ("marcar_como_ativo", "marcar_como_inativo")
    date_hierarchy = "data_publi"
    ordering = ("-data_publi", "titulo_aviso")
    list_per_page = 25





@admin.register(Professor)
class ProfessoresAdmin(StatusActionsMixin, admin.ModelAdmin):
    status_field = "status_professor"
    list_display = ("nome_professor", "email", "status_professor")
    list_editable = ("status_professor",)
    list_filter = ("status_professor",)
    search_fields = ("nome_professor", "email")
    fields = ("nome_professor", "email", "status_professor")
    actions = ("marcar_como_ativo", "marcar_como_inativo")
    ordering = ("nome_professor",)
    list_per_page = 25


@admin.register(HorarioAula)
class HorarioAulaAdmin(admin.ModelAdmin):

    list_display = (
        "id_horario",
        "curso",
        "ano_semestre",
        "turma",
        "turno",
        "sala",
        "horario",
        "dia",
        "nome_aula"
    )

    search_fields = (
        "curso",
        "ano_semestre",
        "turma",
        "sala",
        "nome_aula"
    )

    list_filter = (
        "curso",
        "turno",
        "sala",
        "dia"
    )

    ordering = (
        "curso",
        "ano_semestre",
        "turno",
        "horario"
    )