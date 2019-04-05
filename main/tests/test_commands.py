import io
from datetime import datetime

from django.core import management
from django.test import TestCase

from main.models import Stock


class CommandTest(TestCase):
    def test_update_stock_price(self):
        stock = Stock.objects.create(name="test stock", description="Test Stock of course", launch_date=datetime.now())
        available_prices = stock.prices.count()
        out = io.StringIO()
        management.call_command("update_stock_price", *[1, 13.23], stdout=out)
        self.assertIn(
            "Successfully updated price for stock: {} to {} at {}".format(
                stock.name, stock.current_price().price, stock.current_price().created_on
            ),
            out.getvalue(),
        )
        self.assertEqual(stock.prices.count(), available_prices + 1)
