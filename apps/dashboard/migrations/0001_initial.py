# Generated for the schema mapped in apps.dashboard.models.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Permissao",
            fields=[
                ("id_nivel_permissao", models.AutoField(primary_key=True, serialize=False)),
                ("tipo_permissao", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "db_table": "permissoes",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Professor",
            fields=[
                ("id_professor", models.AutoField(primary_key=True, serialize=False)),
                ("nome_professor", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=150, null=True, unique=True)),
                (
                    "status_professor",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "professor",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Turma",
            fields=[
                ("id_turma", models.AutoField(primary_key=True, serialize=False)),
                ("curso_turma", models.CharField(max_length=100)),
                ("ano_escolar", models.IntegerField()),
                ("turno_turma", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "turma",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Disciplina",
            fields=[
                ("id_disciplina", models.AutoField(primary_key=True, serialize=False)),
                ("nome_disciplina", models.CharField(max_length=100)),
                (
                    "status_disciplina",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "disciplina",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Aviso",
            fields=[
                ("id_aviso", models.AutoField(primary_key=True, serialize=False)),
                ("titulo_aviso", models.CharField(max_length=100)),
                ("mensagem", models.TextField()),
                ("data_publi", models.DateField(blank=True, null=True)),
                ("data_expi", models.DateField(blank=True, null=True)),
                (
                    "status_aviso",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "avisos",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Evento",
            fields=[
                ("id_evento", models.AutoField(primary_key=True, serialize=False)),
                ("titulo_evento", models.CharField(max_length=100)),
                ("descricao", models.TextField()),
                ("evento_horario", models.DateTimeField()),
                (
                    "status_evento",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "db_table": "eventos",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("id_usuario", models.AutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=150, unique=True)),
                ("senha", models.CharField(max_length=255)),
                ("data_criacao", models.DateField(blank=True, null=True)),
                ("ultimo_login", models.DateTimeField(blank=True, null=True)),
                (
                    "status_usu",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
                (
                    "nivel_permissao",
                    models.ForeignKey(
                        blank=True,
                        db_column="id_nivel_permissao",
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="dashboard.permissao",
                    ),
                ),
                (
                    "turma",
                    models.ForeignKey(
                        blank=True,
                        db_column="id_turma",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="dashboard.turma",
                    ),
                ),
            ],
            options={
                "db_table": "usuario",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Horario",
            fields=[
                ("id_horario", models.AutoField(primary_key=True, serialize=False)),
                (
                    "dia_semana",
                    models.CharField(
                        choices=[
                            ("segunda", "Segunda"),
                            ("terca", "Terca"),
                            ("quarta", "Quarta"),
                            ("quinta", "Quinta"),
                            ("sexta", "Sexta"),
                        ],
                        max_length=20,
                    ),
                ),
                ("numero_periodo", models.IntegerField()),
                ("horario_inicio", models.TimeField()),
                ("horario_fim", models.TimeField()),
                (
                    "status_horario",
                    models.CharField(
                        choices=[("ativo", "Ativo"), ("inativo", "Inativo")],
                        default="ativo",
                        max_length=10,
                    ),
                ),
                (
                    "disciplina",
                    models.ForeignKey(
                        db_column="id_disciplina",
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="dashboard.disciplina",
                    ),
                ),
                (
                    "professor",
                    models.ForeignKey(
                        db_column="id_professor",
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="dashboard.professor",
                    ),
                ),
                (
                    "turma",
                    models.ForeignKey(
                        db_column="id_turma",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.turma",
                    ),
                ),
            ],
            options={
                "db_table": "horario",
                "managed": False,
                "unique_together": {("turma", "dia_semana", "numero_periodo")},
            },
        ),
    ]
