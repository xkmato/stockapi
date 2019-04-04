from rest_framework import routers

from main.views import StockViewSet

router = routers.DefaultRouter()
router.register(r'stocks', StockViewSet)
