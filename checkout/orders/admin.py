from django.contrib import admin
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

from .models import Order, Item


class ItemInline(admin.TabularInline):
    model = Item
    readonly_fields = ['unit_price']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [ItemInline]
    list_display = ['id', 'status', 'amount', 'created']
    readonly_fields = ['amount', 'created', 'modified']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        if not change:
            expression = ExpressionWrapper(
                F('quantity') * F('unit_price'), output_field=DecimalField()
            )
            aggregate = form.instance.items.aggregate(amount=expression)
            form.instance.amount = aggregate['amount']
            form.save()
