from rest_framework import serializers

from .models import Client, Address

class ClientSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'full_name',
            'email',
            'any_phone'
        )

class ClientSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'