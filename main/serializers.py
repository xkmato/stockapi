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

    class Meta:
        model = Stock
        fields = "name", "description", "launch_date", "prices", "directors", "current_price"

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

    def get_current_price(self, obj):
        if obj.current_price():
            return obj.current_price().price
