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

class PriceDetailSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source='user.get_fullname', read_only=True)
    period_name = serializers.CharField(source='period.name', read_only=True)
    period_days = serializers.CharField(source='period.days', read_only=True)

    class Meta:
        model = Price
        exclude = ['user', 'item', 'period', 'updated']

class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'

class PriceCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        exclude = ['created', 'updated', 'user']

class ItemCreationSerializer(serializers.ModelSerializer):
    item_price = serializers.CharField(max_length=200)

    def create(self, validated_data):
        pricing = json.loads(validated_data.pop('item_price'))
        item_instance = Item.objects.create(**validated_data)
        for item in pricing:
            Price.objects.create(item=item_instance, user=item_instance.user, current=True,
                                 price=Decimal(item.get('price')), period_id=item.get('period'))
        return item_instance

    class Meta:
        model = Item
        fields = ['name', 'description', 'sku', 'picture', 'category', 'item_price']

class ItemUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        exclude = ['active', 'user']

class ItemListSerializer(serializers.ModelSerializer):
    current_prices = PriceSerializer(many=True, read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'name', 'sku', 'category_name', 'current_prices', 'icon']


class StaticsSerializer(serializers.Serializer):
    customers_total = serializers.IntegerField()


class ItemDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    username = serializers.CharField(source='user.get_full_name')
    item_price = serializers.StringRelatedField(many=True, source='current_prices')

    class Meta:
        model = Item
        fields = ['name', 'description', 'sku', 'picture', 'category_name', 'username', 'created', 'item_price', 'category', 'id']


