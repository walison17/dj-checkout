from django.db import models

from model_utils.models import TimeStampedModel, UUIDModel


class Order(UUIDModel, TimeStampedModel):
    ORDER_PLACED = 0
    COMPLETED = 1
    CANCELED = 2
    STATUSES = (
        (ORDER_PLACED, 'Pedido realizado'),
        (COMPLETED, 'Concluído'),
        (CANCELED, 'Cancelado')
    )

    amount = models.DecimalField(
        'Valor total',
        max_digits=7,
        decimal_places=2,
        null=True,
        editable=False
    )
    status = models.PositiveSmallIntegerField(
        'Situação', choices=STATUSES, default=ORDER_PLACED
    )

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)


class Item(TimeStampedModel):
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    unit_price = models.DecimalField(
        'Preço unitário', max_digits=5, decimal_places=2, editable=False
    )
    service = models.ForeignKey(
        'services.Service',
        verbose_name='Serviço',
        related_name='order_items',
        on_delete=models.PROTECT
    )
    order = models.ForeignKey(
        Order,
        verbose_name='Pedido',
        related_name='items',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'itens'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.quantity}x {self.service}'

    def save(self, *args, **kwargs):
        self.unit_price = self.service.price
        return super().save(*args, **kwargs)
