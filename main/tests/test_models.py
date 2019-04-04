from datetime import datetime

from django.test import TestCase

from main.models import Stock


class StockTests(TestCase):
    def setUp(self) -> None:
        self.stock1 = Stock.objects.create(name='stock1', description='This is a test stock',
                                           launch_date=datetime.now())
        self.stock2 = Stock.objects.create(name='stock2', description='This is another test stock',
                                           launch_date=datetime.now())

    def test_update_stock_price(self):
        available_stock1_prices = self.stock1.prices.count()
        available_stock2_prices = self.stock2.prices.count()
        self.stock1.update_price(11.2)
        self.assertEqual(self.stock1.prices.count(), available_stock1_prices+1)
        self.assertEqual(self.stock2.prices.count(), available_stock2_prices)
        self.stock2.update_price(54.9)
        self.assertEqual(self.stock2.prices.count(), available_stock2_prices+1)

    def test_update_stock_directors(self):
        available_stock1_directors = self.stock1.directors.count()
        available_stock2_directors = self.stock2.directors.count()
        self.stock1.add_director("Test Director")
        self.assertEqual(self.stock1.directors.count(), available_stock1_directors+1)
        self.assertEqual(self.stock2.directors.count(), available_stock2_directors)
        self.stock2.add_director("Another Test Director")
        self.assertEqual(self.stock2.directors.count(), available_stock2_directors+1)
