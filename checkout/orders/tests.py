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
