from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    items = serializers.IntegerField(source="items_in_category", read_only=True)

    class Meta:
       model = Category
       fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = '__all__'

class ItemCreationSerializer(serializers.ModelSerializer):
    item_price = serializers.CharField()

    def create(self, validated_data):
        price = validated_data.pop('item_price')
        item_instance = Item.objects.create(**validated_data)
        Price.objects.create(item=item_instance, price=price, user=item_instance.user, current=True)
        return item_instance

    class Meta:
        model = Item
        fields = ['name', 'description', 'sku', 'picture', 'category', 'item_price']

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'sku', 'category_name', 'current_price', 'icon']