from django.contrib import admin

from main.models import Stock, Price, Director


class StockPriceInline(admin.StackedInline):
    model = Price


class DirectorInline(admin.StackedInline):
    model = Director


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    inlines = StockPriceInline, DirectorInline
