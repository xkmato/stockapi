from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework import viewsets

from main.models import Stock
from main.serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (TokenHasReadWriteScope,)
    authentication_classes = (OAuth2Authentication,)
