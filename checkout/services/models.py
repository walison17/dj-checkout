from django.db import models

from model_utils.models import TimeStampedModel, UUIDModel


class Service(UUIDModel, TimeStampedModel):
    description = models.CharField('Descrição', max_length=100)
    price = models.DecimalField('Preço', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'
        ordering = ('-description',)

    def __str__(self):
        return self.description
