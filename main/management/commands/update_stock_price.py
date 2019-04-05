from datetime import datetime

from django.core.management import BaseCommand

from main.models import Stock


class Command(BaseCommand):
    help = "To update a stock price"

    def add_arguments(self, parser):
        parser.add_argument("stock_id", type=int, help="The ID of the stock that you want to update")
        parser.add_argument("price", type=float, help="The new stock price")

    def handle(self, *args, **options):
        stock_id = options.get("stock_id")
        price = options.get("price")

        stock = Stock.objects.get(pk=stock_id)
        stock.update_price(price)
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully updated price for stock: {} to {} at {}".format(
                    stock.name, stock.current_price().price, stock.current_price().created_on
                )
            )
        )
