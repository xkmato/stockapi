from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    OAuth2Authentication,
)
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from main.models import Stock
from main.serializers import StockSerializer, PriceSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
    To list all stocks and their prices

    GET `/stocks/` will give you a list of all stock. And for each stock, the prices
    GET `/stocks/` will give you a list of all stocks for that day
    GET `/stocks/<pk>/price_list/` will give you a list of prices for a specific stock

    POST `/stocks/` will update stock of that name or create a new stock. Provide it with a list of prices in order to
    update prices
    """

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (TokenHasReadWriteScope,)
    authentication_classes = (OAuth2Authentication,)

    @detail_route()
    def price_list(self, request, pk=None):
        stock = self.get_object()
        prices = stock.prices.all()
        price_data = PriceSerializer(prices, many=True)
        return Response(price_data.data)
