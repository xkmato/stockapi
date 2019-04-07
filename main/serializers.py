from datetime import datetime

from rest_framework import serializers

from main.models import Price, Stock, Director


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "price", "created_on"


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("name",)


class StockSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, required=False)
    directors = DirectorSerializer(many=True, required=False)
    current_price = serializers.SerializerMethodField()
    highest_price = serializers.SerializerMethodField()
    lowest_price = serializers.SerializerMethodField()
    closing_price = serializers.SerializerMethodField()
    opening_price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = "name", "description", "launch_date", "prices", "directors", "current_price", "highest_price", \
                 "lowest_price", "closing_price", "opening_price"

    def create(self, validated_data):
        # Todo request data rejected by drf .is_valid method. Why??
        request = self.context["request"]
        prices_data = request.data.getlist("prices")
        directors_data = request.data.getlist("directors")

        if Stock.objects.filter(name=validated_data["name"]).exists():
            stock = Stock.objects.get(name=validated_data["name"])
        else:
            stock = Stock.objects.create(**validated_data)

        for price_data in prices_data:
            Price.objects.create(stock=stock, **eval(price_data))
        for director_data in directors_data:
            Director.objects.create(stock=stock, **eval(director_data))
        return stock

    def _get_date_from_request(self) -> datetime.date:
        request = self.context['request']
        if request.GET.get('date'):
            date = datetime.strptime(request.GET.get('date'), "%Y-%m-%d").date()
        else:
            date = datetime.now().date()
        return date

    def get_current_price(self, obj):
        if obj.current_price():
            return obj.current_price().price

    def get_highest_price(self, obj):
        date = self._get_date_from_request()
        if obj.day_highest_price(date):
            return obj.day_highest_price(date).price

    def get_lowest_price(self, obj):
        date = self._get_date_from_request()
        if obj.day_lowest_price(date):
            return obj.day_highest_price(date).price

    def get_closing_price(self, obj):
        date = self._get_date_from_request()
        if obj.day_opening_price(date):
            return obj.day_highest_price(date).price

    def get_opening_price(self, obj):
        date = self._get_date_from_request()
        if obj.day_opening_price(date):
            return obj.day_highest_price(date).price
