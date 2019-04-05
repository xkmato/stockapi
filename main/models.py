from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Stock(TimeStampedModel):
    name = models.CharField(max_length=60)
    description = models.TextField()
    launch_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def update_price(self, price):
        Price.objects.create(price=price, stock=self)

    def add_director(self, name):
        Director.objects.create(name=name, stock=self)

    def prices_of_date(self, date):
        start_time = datetime.combine(date, datetime.min.time())
        end_time = start_time + timedelta(hours=24)
        return self.prices.filter(created_on__gte=start_time, created_on__lt=end_time)

    def day_highest_price(self, date):
        return self.prices_of_date(date).order_by("-price").first()

    def day_lowest_price(self, date):
        return self.prices_of_date(date).order_by("price").first()

    def day_closing_price(self, date):
        return self.prices_of_date(date).latest("created_on")

    def day_opening_price(self, date):
        return self.prices_of_date(date).earliest("created_on")

    def current_price(self):
        return self.prices.latest("created_on")


class Director(TimeStampedModel):
    name = models.CharField(max_length=60)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="directors")


class Price(TimeStampedModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="prices")
    price = models.DecimalField(decimal_places=2, max_digits=8)

    def __str__(self):
        return self.stock.name

    class Meta:
        ordering = ("created_on",)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
