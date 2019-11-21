from django.test import TestCase
from decimal import Decimal

from model_bakery import baker

from .models import Order, Item


class TestOrderModel(TestCase):
    def setUp(self):
        self.order = baker.make(Order)

    def test_calculate_amount(self):
        item1 = baker.make(Item, quantity=2, service__price=Decimal(1.5))
        item2 = baker.make(Item, quantity=1, service__price=Decimal(1.2))
        self.order.items.set([item1, item2])

        self.assertTrue(
            self.order.calculate_amount().compare(Decimal(4.2))
        )


class TestItemModel(TestCase):
    def setUp(self):
        self.service = baker.make('services.Service', price=Decimal(8))

    def test_set_unit_price_on_save(self):
        item = baker.make(Item, quantity=2, service=self.service)

        self.assertEqual(item.unit_price, self.service.price)

    def test_must_not_update_unit_price_when_item_is_already_created(self):
        item = baker.make(Item, quantity=2, service=self.service)

        original_price = self.service.price

        # set new service price
        self.service.price = Decimal(8.5)
        self.service.save()

        # update item quantity
        item.quantity = 2
        item.save()

        self.assertEqual(item.unit_price, original_price)
