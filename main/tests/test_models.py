from datetime import datetime, timedelta

from django.test import TestCase

from main.models import Stock


class StockTests(TestCase):
    def setUp(self) -> None:
        self.stock1 = Stock.objects.create(
            name="stock1",
            description="This is a test stock",
            launch_date=datetime.now(),
        )
        self.stock2 = Stock.objects.create(
            name="stock2",
            description="This is another test stock",
            launch_date=datetime.now(),
        )

    def test_update_stock_price(self):
        available_stock1_prices = self.stock1.prices.count()
        available_stock2_prices = self.stock2.prices.count()
        self.stock1.update_price(11.2)
        self.assertEqual(self.stock1.prices.count(), available_stock1_prices + 1)
        self.assertEqual(self.stock2.prices.count(), available_stock2_prices)
        self.stock2.update_price(54.9)
        self.assertEqual(self.stock2.prices.count(), available_stock2_prices + 1)

    def test_update_stock_directors(self):
        available_stock1_directors = self.stock1.directors.count()
        available_stock2_directors = self.stock2.directors.count()
        self.stock1.add_director("Test Director")
        self.assertEqual(self.stock1.directors.count(), available_stock1_directors + 1)
        self.assertEqual(self.stock2.directors.count(), available_stock2_directors)
        self.stock2.add_director("Another Test Director")
        self.assertEqual(self.stock2.directors.count(), available_stock2_directors + 1)

    def test_prices_of_date(self):
        self.stock1.update_price(12.13)
        self.stock1.update_price(12.14)
        self.stock1.update_price(12.20)
        self.stock1.update_price(13.21)
        self.stock1.update_price(13.25)
        self.stock1.update_price(14.05)

        # Manually change first 3 prices to yesterday
        for price in self.stock1.prices.all()[:3]:
            yest_created_on = price.created_on - timedelta(hours=25)
            price.created_on = yest_created_on
            price.save()

        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        self.assertEqual(self.stock1.prices_of_date(today).count(), 3)
        self.assertEqual(self.stock1.prices_of_date(yesterday).count(), 3)

    def test_day_highest_price(self):
        self.stock1.update_price(12.13)
        self.stock1.update_price(12.14)
        self.stock1.update_price(12.20)
        self.stock1.update_price(13.21)
        self.stock1.update_price(13.25)
        self.stock1.update_price(14.05)
        self.assertEqual(
            float(self.stock1.day_highest_price(datetime.now().date()).price), 14.05
        )

    def test_day_lowest_price(self):
        self.stock1.update_price(12.13)
        self.stock1.update_price(12.14)
        self.stock1.update_price(12.20)
        self.stock1.update_price(13.21)
        self.stock1.update_price(13.25)
        self.stock1.update_price(14.05)
        self.assertEqual(
            float(self.stock1.day_lowest_price(datetime.now().date()).price), 12.13
        )

    def test_day_closing_price(self):
        self.stock1.update_price(12.13)
        self.stock1.update_price(12.14)
        self.stock1.update_price(12.20)
        self.stock1.update_price(13.21)
        self.stock1.update_price(13.25)
        self.stock1.update_price(14.05)
        self.assertEqual(
            float(self.stock1.day_closing_price(datetime.now().date()).price), 14.05
        )

    def test_day_opening_price(self):
        self.stock1.update_price(12.13)
        self.stock1.update_price(12.14)
        self.stock1.update_price(12.20)
        self.stock1.update_price(13.21)
        self.stock1.update_price(13.25)
        self.stock1.update_price(14.05)
        self.assertEqual(
            float(self.stock1.day_opening_price(datetime.now().date()).price), 12.13
        )

    def test_current_price(self):
        self.stock1.update_price(12.13)
        self.stock1.update_price(12.14)
        self.stock1.update_price(12.20)
        self.stock1.update_price(13.21)
        self.stock1.update_price(13.25)
        self.stock1.update_price(14.05)
        self.assertEqual(float(self.stock1.current_price().price), 14.05)
