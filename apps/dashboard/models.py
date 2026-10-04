from datetime import datetime, timedelta, time
from django.db import models



STATUS_CHOICES = (
    ("ativo", "Ativo"),
    ("inativo", "Inativo"),
)

DIA_SEMANA_CHOICES = (
    ("segunda", "Segunda"),
    ("terca", "Terca"),
    ("quarta", "Quarta"),
    ("quinta", "Quinta"),
    ("sexta", "Sexta"),
)


class Turma(models.Model):
    id_turma = models.AutoField(primary_key=True)
    curso_turma = models.CharField(max_length=100)
    ano_escolar = models.IntegerField()
    turno_turma = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "turma"

    def __str__(self):
        return f"{self.curso_turma} - {self.ano_escolar}o ano - {self.turno_turma}"


class Permissao(models.Model):
    id_nivel_permissao = models.AutoField(primary_key=True)
    tipo_permissao = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = "permissoes"

    def __str__(self):
        return self.tipo_permissao


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    senha = models.CharField(max_length=255)

    data_criacao = models.DateField(null=True, blank=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)
    nivel_permissao = models.ForeignKey(
        Permissao,
        on_delete=models.RESTRICT,
        db_column="id_nivel_permissao",
        null=True,
        blank=True,
    )
    status_usu = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ativo")

    class Meta:
        managed = False
        db_table = "usuario"

    def __str__(self):
        return self.nome




class HorarioAula(models.Model):

    id_horario = models.AutoField(
        primary_key=True,
        db_column="id_horario"
    )

    curso = models.CharField(
        max_length=20,
        db_column="curso"
    )

    ano_semestre = models.CharField(
        max_length=30,
        db_column="ano_semestre"
    )

    turma = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        db_column="turma"
    )

    turno = models.CharField(
        max_length=20,
        db_column="turno"
    )

    sala = models.CharField(
        max_length=30,
        db_column="sala"
    )

    horario = models.CharField(
        max_length=30,
        db_column="horario"
    )

    dia = models.IntegerField(
        db_column="dia"
    )

    nome_aula = models.CharField(
        max_length=200,
        db_column="nome_aula"
    )

    class Meta:
        managed = False
        db_table = "horario_aula"



class Dataimpor(models.Model):

    titulo = models.CharField(max_length=200)

    descricao = models.TextField(
        blank=True,
        null=True
    )

    data = models.DateField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        managed = False
        db_table = 'dataimpor'

    def __str__(self):
        return self.titulo


class Disciplina(models.Model):
    id_disciplina = models.AutoField(primary_key=True)
    nome_disciplina = models.CharField(max_length=100)
    status_disciplina = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ativo")

    class Meta:
        managed = False
        db_table = "disciplina"

    def __str__(self):
        return self.nome_disciplina


class Aviso(models.Model):
    id_aviso = models.AutoField(primary_key=True)
    titulo_aviso = models.CharField(max_length=100)
    data_publi = models.DateField(null=True, blank=True)
    data_expi = models.DateField(null=True, blank=True)
    status_aviso = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ativo")

    class Meta:
        managed = False
        db_table = "avisos"

    def __str__(self):
        return self.titulo_aviso

class Evento(models.Model):

    id_evento = models.AutoField(
        primary_key=True
    )

    titulo = models.CharField(
        max_length=150
    )

    descricao = models.TextField()

    data_inicio = models.DateField()

    data_fim = models.DateField()

    hora_inicio = models.TimeField()

    hora_fim = models.TimeField()

    imagem = models.ImageField(
        upload_to='eventos/',
        blank=True,
        null=True
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'eventos'
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'


class Evento_OLD(models.Model):

    id_evento = models.AutoField(
        primary_key=True,
        db_column="id_evento"
    )

    titulo = models.CharField(
        max_length=200
    )

    descricao = models.TextField()

    imagem = models.ImageField(
        upload_to="eventos/",
        blank=True,
        null=True
    )

    data_criacao = models.DateTimeField()

    class Meta:

        managed = False
        db_table = "evento"


class Professor(models.Model):
    id_professor = models.AutoField(primary_key=True)
    nome_professor = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    status_professor = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ativo")

    class Meta:
        managed = False
        db_table = "professor"
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_professor


class InformacaoOperacional(models.Model):

    id_info = models.AutoField(
        primary_key=True,
        db_column="id_info"
    )

    data_lancamento = models.DateField(
        db_column="data_lancamento"
    )

    titulo = models.CharField(
        max_length=200,
        db_column="titulo"
    )

    categoria = models.CharField(
        max_length=100,
        db_column="categoria"
    )

    class Meta:

        managed = False

        db_table = "informacao_operacional"

    def __str__(self):

        return self.titulo



class Lembrete(models.Model):

    STATUS_CHOICES = [
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
    ]

    id_lembrete = models.AutoField(
        primary_key=True
    )

    titulo_lembrete = models.CharField(
        max_length=100
    )

    conteudo_lembrete = models.TextField()



    data_publi = models.DateField(
        auto_now_add=True
    )

    data_expi = models.DateField(
        null=True,
        blank=True
    )

    fixado = models.BooleanField(
        default=False
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ATIVO'
    )

    class Meta:
        managed = False
        db_table = "lembretes"
        verbose_name = "Lembrete"
        verbose_name_plural = "Lembretes"


    def __str__(self):
        return self.titulo_lembrete


class Cardapio(models.Model):

    id_cardapio = models.AutoField(
        primary_key=True
    )

    dia_semana = models.CharField(
        max_length=30
    )

    lanche = models.CharField(
        max_length=100
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        managed = False

        db_table = "cardapio"