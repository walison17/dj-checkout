from django.contrib import admin

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
            form.instance.amount = form.instance.calculate_amount()
            form.save()
