from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from main.models import Stock, Price, Director


class StockViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='test', password='test123', is_superuser=True)
        self.stock1 = Stock.objects.create(name='stock1', description='This is a test stock',
                                           launch_date=datetime.now())
        self.stock2 = Stock.objects.create(name='stock2', description='This is another test stock',
                                           launch_date=datetime.now())

        self.stock1.update_price(13.12)
        self.stock1.update_price(13.13)
        self.stock1.add_director("Director1")
        self.stock1.add_director("Director2")

        self.stock2.update_price(43.21)
        self.stock2.update_price(43.22)
        self.stock2.add_director("Director3")
        self.stock2.add_director("Director4")

    def test_list_stocks(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.get('/stocks/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Stock.objects.count())

        prices, directors = 0, 0
        for stock in response.json():
            prices += len(stock['prices'])
            directors += len(stock['directors'])

        self.assertEqual(Price.objects.count(), prices)
        self.assertEqual(Director.objects.count(), prices)

    def test_post_stocks(self):
        prices = [dict(price=13.67), dict(price=14.56)]
        directors = [dict(name='Director Test1'), dict(name='Director Test2')]
        data = dict(prices=prices, directors=directors, name='test name2', description="This is a test description 1",
                    launch_date=datetime.now().isoformat())


        stock_count = Stock.objects.count()
        price_count = Price.objects.count()
        director_count = Director.objects.count()

        #Check Authentication
        client = APIClient()
        response = client.post('/stocks/', data=data)
        self.assertEqual(response.status_code, 401)
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = client.post('/stocks/', data=data)
        print(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stock.objects.count(), stock_count+1)
        self.assertEqual(Price.objects.count(), price_count+2)
        self.assertEqual(Director.objects.count(), director_count+2)
