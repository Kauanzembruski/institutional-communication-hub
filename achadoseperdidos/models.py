from django.db import models


class ItemAchado(models.Model):

    nome = models.CharField(
        max_length=150
    )

    imagem = models.ImageField(
        upload_to='achados/',
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        managed = False
        db_table = 'itens_achados'

        verbose_name = 'Item Achado'
        verbose_name_plural = 'Itens Achados'

        ordering = ['-criado_em']

    def __str__(self):

        return self.nome