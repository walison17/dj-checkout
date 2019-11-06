from django.contrib import admin
from django.db.models import Sum

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
            aggregate = form.instance.items.aggregate(Sum('unit_price'))
            form.instance.amount = aggregate['unit_price__sum']
            form.save()
