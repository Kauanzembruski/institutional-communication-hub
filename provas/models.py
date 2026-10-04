from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Prova(models.Model):

    CURSOS = [

        ('TII', 'TII'),
        ('ADM', 'ADM'),
        ('ADS', 'ADS'),
        ('TPG', 'TPG'),

    ]

    curso = models.CharField(
        max_length=10,
        choices=CURSOS
    )

    disciplina = models.CharField(
        max_length=100
    )

    turma = models.CharField(
        max_length=50
    )

    data = models.DateField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        managed = False
        db_table = 'provas'

        ordering = ['data']

        verbose_name = 'Prova'
        verbose_name_plural = 'Provas'

    def clean(self):

        if self.data < date.today():

            raise ValidationError({
                'data': 'Não é permitido cadastrar datas anteriores.'
            })

    def save(self, *args, **kwargs):

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.disciplina} - {self.turma}'