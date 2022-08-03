from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.ModelSerializer):
    items = serializers.IntegerField(source="items_in_category", read_only=True)

    class Meta:
       model = Category
       fields = '__all__'