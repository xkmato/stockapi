from rest_framework import serializers

from main.models import Price, Stock, Director


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = 'price', 'created_on',


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name',


class StockSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True)
    directors = DirectorSerializer(many=True)
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = 'name', 'description', 'launch_date', 'current_price', 'prices', 'directors',

    def create(self, validated_data):
        prices_data = validated_data.pop('prices')
        stock = Stock.objects.get_or_create(**validated_data)
        for price_data in prices_data:
            Price.objects.create(stock=stock, **price_data)
        return stock

    def get_current_price(self, obj):
        if obj.current_price():
            return obj.current_price().price
