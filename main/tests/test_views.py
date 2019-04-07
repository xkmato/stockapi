from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from oauth2_provider.models import Application, AccessToken
from rest_framework.test import APIClient

from main.models import Stock, Price, Director


class StockViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test", password="test123", is_superuser=True)
        self.user1 = User.objects.create(username="test1", password="test123", is_superuser=True)
        self.stock1 = Stock.objects.create(
            name="stock1", description="This is a test stock", launch_date=datetime.now()
        )
        self.stock2 = Stock.objects.create(
            name="stock2", description="This is another test stock", launch_date=datetime.now()
        )

        self.stock1.update_price(13.12)
        self.stock1.update_price(13.13)
        self.stock1.add_director("Director1")
        self.stock1.add_director("Director2")

        self.stock2.update_price(43.21)
        self.stock2.update_price(43.22)
        self.stock2.add_director("Director3")
        self.stock2.add_director("Director4")

        self.app = Application(
            name="Test App",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.app.save()

        self.token = AccessToken.objects.create(
            user=self.user,
            token="123456789",
            application=self.app,
            scope="read write",
            expires=timezone.now() + timedelta(days=1),
        )

        self.token1 = AccessToken.objects.create(
            user=self.user1,
            token="12345678911",
            application=self.app,
            scope="read",
            expires=timezone.now() + timedelta(days=1),
        )

        self.auth_write = "Bearer {}".format(self.token.token)
        self.auth_read = "Bearer {}".format(self.token1.token)

    def test_list_stocks(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.auth_read)
        response = client.get("/stocks/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Stock.objects.count())

        prices, directors = 0, 0
        for stock in response.json():
            prices += len(stock["prices"])
            directors += len(stock["directors"])

        self.assertEqual(Price.objects.count(), prices)
        self.assertEqual(Director.objects.count(), prices)

    def test_post_stocks(self):
        prices = [dict(price=13.67), dict(price=14.56)]
        directors = [dict(name="Director Test1"), dict(name="Director Test2")]
        data = dict(
            prices=prices,
            directors=directors,
            name="test name2",
            description="This is a test description 1",
            launch_date=datetime.now().isoformat(),
        )

        stock_count = Stock.objects.count()
        price_count = Price.objects.count()
        director_count = Director.objects.count()

        client = APIClient()
        # Can't write with only read access
        client.credentials(HTTP_AUTHORIZATION=self.auth_read)
        response = client.post("/stocks/", data=data)
        self.assertEqual(response.status_code, 403)
        client.credentials(HTTP_AUTHORIZATION=self.auth_write)

        response = client.post("/stocks/", data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Stock.objects.count(), stock_count + 1)
        self.assertEqual(Price.objects.count(), price_count + 2)
        self.assertEqual(Director.objects.count(), director_count + 2)

    def test_price_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.auth_read)
        response = client.get("/stocks/{}/price_list/".format(self.stock1.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), self.stock1.prices.count())
        self.assertListEqual(response.json(), [{"price": str(p.price), "created_on": p.created_on.isoformat().
                             replace("+00:00", "Z")} for p in self.stock1.prices.all()])
