from decimal import Decimal

from rest_framework import serializers
from rest_framework.utils import json

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    items = serializers.IntegerField(source="items_in_category", read_only=True)

    class Meta:
       model = Category
       fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['price', 'period_days']

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

class ItemCreationSerializer(serializers.ModelSerializer):
    item_price = serializers.CharField(max_length=200)

    def create(self, validated_data):
        print(validated_data)
        pricing = json.loads(validated_data.pop('item_price'))
        item_instance = Item.objects.create(**validated_data)
        for item in pricing:
            Price.objects.create(item=item_instance, user=item_instance.user, current=True,
                                 price=Decimal(item.get('price')), period_id=item.get('period'))
        return item_instance

    class Meta:
        model = Item
        fields = ['name', 'description', 'sku', 'picture', 'category', 'item_price']

class ItemListSerializer(serializers.ModelSerializer):
    current_prices = PriceSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'sku', 'category_name', 'current_prices', 'icon']


class StaticsSerializer(serializers.Serializer):
    customers_total = serializers.IntegerField()


