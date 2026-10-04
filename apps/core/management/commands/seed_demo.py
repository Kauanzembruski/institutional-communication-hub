from datetime import time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.dashboard.models import Aviso, Disciplina, Evento, Horario, Permissao, Professor, Turma, Usuario


class Command(BaseCommand):
    help = "Cria dados demonstrativos para o mural institucional."

    def handle(self, *args, **options):
        now = timezone.now()
        today = timezone.localdate()

        turma, _ = Turma.objects.get_or_create(
            curso_turma="Informatica",
            ano_escolar=1,
            turno_turma="Manha",
        )
        permissao, _ = Permissao.objects.get_or_create(tipo_permissao="Administrador")
        usuario, _ = Usuario.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "nome": "Administrador Demo",
                "senha": "senha-demo",
                "turma": turma,
                "nivel_permissao": permissao,
                "data_criacao": today,
                "status_usu": "ativo",
            },
        )
        professor, _ = Professor.objects.get_or_create(
            email="professor@example.com",
            defaults={
                "nome_professor": "Professor Demo",
                "status_professor": "ativo",
            },
        )
        disciplina, _ = Disciplina.objects.get_or_create(
            nome_disciplina="Matematica",
            defaults={
                "status_disciplina": "ativo",
            },
        )

        usuario.ultimo_login = now
        usuario.save(update_fields=["ultimo_login"])

        Aviso.objects.get_or_create(
            titulo_aviso="Renovacao de matricula aberta",
            defaults={
                "mensagem": "O periodo de rematricula esta aberto no sistema academico.",
                "data_publi": today,
                "data_expi": today + timedelta(days=20),
                "status_aviso": "ativo",
            },
        )
        Evento.objects.get_or_create(
            titulo_evento="Semana Academica",
            defaults={
                "descricao": "Palestras, oficinas e apresentacoes de projetos.",
                "evento_horario": now + timedelta(days=10),
                "status_evento": "ativo",
            },
        )
        Horario.objects.get_or_create(
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            dia_semana="segunda",
            numero_periodo=1,
            defaults={
                "horario_inicio": time(8, 0),
                "horario_fim": time(9, 40),
                "status_horario": "ativo",
            },
        )

        self.stdout.write(self.style.SUCCESS("Dados demonstrativos criados com sucesso."))
